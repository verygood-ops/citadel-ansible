# Citadel

An ansible lookup_plugin and module that implements a simple secrets management store for teams and organizations, backed by Amazon's S3 and IAM APIs.

Inspired by [Noah Kantrowitz](https://github.com/coderanger)'s [poise/citadel](https://github.com/poise/citadel). [See here for his blog post](https://coderanger.net/chef-secrets/).

## Installation

### Dependencies

Requires: `boto`

### Installation Options

As per [Ansible's recommendations for distributing plugins](http://docs.ansible.com/developing_plugins.html#distributing-plugins), it is recommended to put common plugins in:

- /usr/share/ansible/plugins, in a subfolder for each plugin type:

  * action_plugins
  * lookup_plugins
  * callback_plugins
  * connection_plugins
  * filter_plugins
  * vars_plugins


- change the [lookup_plugins](http://docs.ansible.com/intro_configuration.html#lookup-plugins) variable in your `ansible.cfg`, which can be placed in any top-level ansible playbook.

- you may also just add the plugin in a top-level playbook, in folders named the same as indicated above.

### Install in `/usr/share/ansible/plugins`

```bash
make install
```

### Install in a target plugin directory

This also works for bundling it.

```bash
make install TARGET='"/your/plugin/directory/here"'
```

Don't forget to check that the `ansible.cfg` in your top-level playbook has the `lookup_plugins` variable set to the path.

## Configuration

### In your `lookup_plugins` directory

Create a python file, `citadel.py` with these contents:

```python
import libcitadel   # should be on your path


class LookupModule(libcitadel.S3LookupModule):
    bucket_var = 'citadel_bucket'
    profile_var = 'citadel_profile'
    region_var = 'citadel_region'
```

### In your YAML files

Wherever you set your var files, you can configure the citadel_bucket as follows:

```yaml
---
  vars:
    citadel_bucket: your-secret-bucket

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

`citadel-ansible` is licensed under the Apache 2.0 license. Please create an issue if this license doesn't work for you.

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

- [@mahmoudimus](https://github.com/mahmoudimus)
- [@victorlin](https://github.com/victorlin)
- [@bninja](https://github.com/bninja)
