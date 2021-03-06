from __future__ import unicode_literals, absolute_import
import os

from ansible.utils import listify
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
import boto.provider
import boto.s3


__all__ = [
    'S3LookupModule'
]


class S3LookupModule(object):

    #: Default bucket. Override with "bucket=".
    bucket = None

    #: Variable name with default bucket.
    bucket_var = None

    #: Default connection profile. Override with "profile=".
    profile = None

    #: Variable name with default connection profile.
    profile_var = None

    #: Default connection region. Override with "region=".
    region = None

    #: Variable name with default connection region.
    region_var = None

    #: Object satisfying `collections.MutableMapping` or None for no caching.
    cache = None

    def cache_key(self, bucket_name, key_name):
        return 's3://{0}{1}'.format(bucket_name, key_name)

    def loads(self, content_type, content):
        return content

    def options(self, inject):
        options = {
            'bucket': self.bucket,
            'profile': self.profile,
            'region': self.region,
        }
        if inject:
            for option, var in [
                ('bucket', self.bucket_var),
                ('profile', self.profile_var),
                ('region', self.region_var),
            ]:
                if var and var in inject:
                    options[option] = inject[var]
        return options

    def run(self, terms, variables=None, **kwargs):
        basedir = self.get_basedir(variables)
        escape = variables.get('escape', False)

        # XXX: https://github.com/ansible/ansible/issues/7370
        terms = listify.listify_lookup_plugin_terms(terms, self._templar, self._loader)

        ret = []

        inject = variables.get('vars', {})
        defaults = self.options(inject)

        for term in terms:
            params = term.split()

            key_name = params[0]

            options = defaults.copy()
            try:
                for param in params[1:]:
                    name, value = param.split('=')
                    assert(name in options)
                    options[name] = value
            except (ValueError, AssertionError), e:
                raise AnsibleError(e)

            # cache
            if self.cache is not None:
                cache_key = self.cache_key(options['bucket'], key_name)
                if cache_key in self.cache:
                    contents = self.cache[cache_key]
                    ret.append(contents)
                    continue

            # connect
            profile_name = options['profile']
            if not profile_name:
                for env_var in ('AWS_DEFAULT_PROFILE', 'AWS_PROFILE'):
                    profile_name = os.environ.get(env_var)
                    if profile_name:
                        break

            cxn = None
            while cxn is None:
                try:
                    if options['region']:
                        cxn = boto.s3.connect_to_region(
                            options['region'], profile_name=profile_name,
                        )
                    else:
                        cxn = boto.connect_s3(profile_name=profile_name)
                except boto.provider.ProfileNotFoundError, e:
                    if profile_name is None:
                        raise AnsibleError('Unable to connect to s3')
                    profile_name = None
                except (boto.exception.BotoClientError, boto.exception.S3ResponseError), e:
                    raise AnsibleError('Unable to connect to s3')
            # read
            # NOTE: lookup deferred (validate=False) so we don't need s3:List* permission
            bucket = cxn.get_bucket(options['bucket'], validate=False)
            key = boto.s3.key.Key(bucket, key_name)
            try:
                contents = key.get_contents_as_string()
            except boto.exception.S3ResponseError, e:
                raise AnsibleError(
                    'Unable to get s3://{bucket}/{key} contents - {code}, {message}'.format(
                        bucket=options['bucket'],
                        key=key_name,
                        code=e.error_code,
                        message=e.message,
                    )
                )
            if escape:
                # if there are newlines in the contents, they are not rendered
                # correctly
                contents = contents.encode('unicode-escape')
            # cache
            if self.cache is not None:
                cache_key = self.cache_key(options['bucket'], key_name)
                self.cache[cache_key] = contents

            ret.append(contents)

        return ret
