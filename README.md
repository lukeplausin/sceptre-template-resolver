# Sceptre Template Resolver
A resolver of templates for Sceptre

## What is Sceptre?

Sceptre is a template deployment engine for AWS cloudformation. It can greatly increase productivity in projects which are spread across multiple cloudformation templates.

[Sceptre Repository](https://github.com/cloudreach/sceptre)

[Sceptre Documentation](https://sceptre.cloudreach.com/latest/docs/get_started.html)

## Install this resolver

To install this resolver, simply run the following command:

`pip install git+https://github.com/lukeplausin/sceptre-template-resolver.git`

## What can this resolver do?

This resolver is useful in any case where you might want to use the output of of one template as the input to another. For example, this resolver can allow you to template a userdata script for an EC2 instance using Jinja2 tags, exactly how you would if using Jinja2 to template your cloudformation.

```yaml
sceptre_user_data:
  ec2_user_data: !template scripts/dynamic_user_data.sh.j2
  instance_directories:
  - home
  - games
  - templates
  - etc
```

In your `scripts/dynamic_user_data.sh.j2` file:
```bash
{% for directory in sceptre_user_data.instance_directories %}
echo "Creating directory {{ directory }}"
mkdir {{ directory }}
{% endfor %}
```

In your actual deployment:
```bash
echo "Creating directory home"
mkdir home
echo "Creating directory games"
mkdir games
echo "Creating directory templates"
mkdir templates
echo "Creating directory etc"
mkdir etc
```

## What are the limitations?

This resolver is based on the Sceptre `template` object. That means that it can resolve any type of template which Sceptre can resolve. At the time of writing, this includes:

- Jinja2 templates
- Python scripts
- Regular files

Unlike the standard `template` object, this resolver does not assume that your template will be in the `templates` directory.

If you use this resolver to resolve a key within the `sceptre_user_data` block of your template, then any references to this key within your template will resolve to a `None` object. This is intentional, to avoid circular dependencies.

Please remember that your `template` file inputs must follow the same rules as regular Sceptre templates. This means they must have a `.j2`, `.yaml` or `.py` extension.
