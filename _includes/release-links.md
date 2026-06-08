{% if table == 'c' %}
  {% assign shortname = 'openslide' %}
  {% assign github = 'openslide' %}
{% else %}
  {% assign shortname = table %}
  {% capture github %}openslide-{{ shortname }}{% endcapture %}
{% endif %}

{% for release in site.data.releases[table] %}
  {% if release.version -%}
    [{{ shortname }}-{{ release.version }}]: https://github.com/openslide/{{ github }}/releases/tag/v{{ release.version }}
  {% endif %}
{% endfor %}
