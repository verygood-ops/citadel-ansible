# Citadel

An ansible module that implements a simple secrets management store for teams and organizations, backed by Amazon's S3 and IAM APIs.

Inspired by [Noah Kantrowitz](https://github.com/coderanger)'s [poise/citadel](https://github.com/poise/citadel). [See here for his blog post](https://coderanger.net/chef-secrets/).

## Installation

## Configuration

### In your YAML files

### As a library

```python
class LookupModule(confu.ansible.S3LookupModule):
    bucket_var = 'citadel_bucket'
    profile_var = 'citadel_profile'
    region_var = 'citadel_region'
```

## Usage

Assuming your secret bucket is called `your-sekret-bucket`, you have proper permissions to read from it (via IAM or credentials, etc), and your secret structure in Amazon's S3 is as follows:

```
your-sekret-bucket
|-- newrelic
│   |-- license_key
```

In your ansible playbooks:

```yaml
newrelic_license_key: "{{ lookup('citadel', '/newrelic/license_key').strip() }}"
```

When ansible processes the yaml files, it will evaluate the lookup function and will fetch the `your-secret-bucket/newrelic/license_key` key, read it and ansible will bind it to the `newrelic_license_key` variable.

License
-------

`ansible-citadel-module` is licensed under the Apache 2.0 license. Please create an issue if this license doesn't work for you.

## Contribute
- Check for open issues or open a fresh issue to start a discussion around a
  feature idea or a bug.
- Fork the repository on GitHub to start making your changes to the master
  branch (or branch off of it).
- Write a test which shows that the bug was fixed or that the feature
  works as expected.
- Send a pull request and bug the maintainer until it gets merged and
  published.
- Make sure to add yourself to the author's file in `setup.py` and the
  `Contributors` section below :)


## Contributors

- `@mahmoudimus <https://github.com/mahmoudimus>`_
- `@victorlin <https://github.com/victorlin>`_
- `@bninja <https://github.com/bninja>`_
