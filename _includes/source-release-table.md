<div class="releases indent">
  <table>
    {% for release in releases %}
      <tr class="{% cycle package: 'odd', 'even' %}">
        <th>
          <a href="https://github.com/openslide/{{ package }}/releases/tag/v{{ release.version }}">
            {{ release.version }}
          </a>
        </th>
        <td>{{ release.date }}</td>
        <td>
          {% if release.gz %}
            <a href="https://github.com/openslide/{{ package }}/releases/download/v{{ release.version }}/{{ package }}-{{ release.version }}.tar.gz">tar.gz</a>
          {% endif %}
        </td>
        <td>
          {% if release.xz %}
            <a href="https://github.com/openslide/{{ package }}/releases/download/v{{ release.version }}/{{ package }}-{{ release.version }}.tar.xz">tar.xz</a>
          {% endif %}
        </td>
        {% if package == 'openslide-python' %}
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
