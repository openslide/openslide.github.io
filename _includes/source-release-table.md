{% assign any_gh = false %}
{% assign any_jar = false %}
{% assign any_whl = false %}
{% for release in releases %}
  {% if release.gh %}
    {% assign any_gh = true %}
  {% endif %}
  {% if release.jar %}
    {% assign any_jar = true %}
  {% endif %}
  {% if release.whl %}
    {% assign any_whl = true %}
  {% endif %}
{% endfor %}

<div class="releases indent">
  <table>
    {% for release in releases %}
      {% if release.src_ %}
        {% capture srcname %}{{ package|replace:'-','_' }}{% endcapture %}
      {% else %}
        {% assign srcname = package %}
      {% endif %}
      <tr class="{% cycle package: 'odd', 'even' %}">
        <th>
          <a href="https://github.com/openslide/{{ package }}/releases/tag/v{{ release.version }}">
            {{ release.version }}
          </a>
        </th>
        <td>{{ release.date }}</td>
        <td>
          {% if release.gz %}
            <a href="https://github.com/openslide/{{ package }}/releases/download/v{{ release.version }}/{{ srcname }}-{{ release.version }}.tar.gz">tar.gz</a>
          {% elsif release.gh %}
            <a href="https://github.com/openslide/{{ package }}/archive/refs/tags/v{{ release.version }}.tar.gz">tar.gz</a>
          {% endif %}
        </td>
        <td>
          {% if release.xz %}
            <a href="https://github.com/openslide/{{ package }}/releases/download/v{{ release.version }}/{{ srcname }}-{{ release.version }}.tar.xz">tar.xz</a>
          {% endif %}
        </td>
        {% if any_gh %}
          <td>
            {% if release.gh %}
              <a href="https://github.com/openslide/{{ package }}/archive/refs/tags/v{{ release.version }}.zip">zip</a>
            {% endif %}
          </td>
        {% endif %}
        {% if any_jar %}
          <td>
            {% if release.jar %}
              <a href="https://github.com/openslide/{{ package }}/releases/download/v{{ release.version }}/{{ package }}-{{ release.version }}.jar">jar</a>
            {% endif %}
          </td>
        {% endif %}
        {% if any_whl %}
          <td>
            {% if release.whl %}
              <a href="https://pypi.org/project/{{ package }}/{{ release.version }}/#files">Wheels (PyPI)</a>
            {% endif %}
          </td>
        {% endif %}
      </tr>
    {% endfor %}
  </table>
</div>
