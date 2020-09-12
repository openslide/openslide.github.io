<div class="releases indent">
  <table>
    {% for release in releases %}
      <tr class="{% cycle package: 'odd', 'even' %}">
        <th>{{ release.version }}</th>
        <td>{{ release.date }}</td>
        <td><a href="https://github.com/openslide/{{ package }}/releases/download/v{{ release.version }}/{{ package }}-{{ release.version }}.tar.gz">tar.gz</a></td>
        <td>
          {% if release.no_xz == null %}
            <a href="https://github.com/openslide/{{ package }}/releases/download/v{{ release.version }}/{{ package }}-{{ release.version }}.tar.xz">tar.xz</a>
          {% endif %}
        </td>
        {% if package == 'openslide-python' %}
          <td>
            {% if release.no_whl == null %}
              <a href="https://pypi.python.org/pypi/{{ package }}/{{ release.version }}#downloads">Wheels (PyPI)</a>
            {% endif %}
          </td>
        {% endif %}
      </tr>
    {% endfor %}
  </table>
</div>
