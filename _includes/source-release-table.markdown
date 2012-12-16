<div class="releases">
  <table>
    {% for release in releases %}
      <tr class="{% cycle package: 'odd', 'even' %}">
        <th>{{ release.version }}</th>
        <td>{{ release.date }}</td>
        <td><a href="https://github.com/downloads/openslide/{{ package }}/{{ package }}-{{ release.version }}.tar.gz">tar.gz</a></td>
        <td>
          {% if release.no_xz == null %}
            <a href="https://github.com/downloads/openslide/{{ package }}/{{ package }}-{{ release.version }}.tar.xz">tar.xz</a>
          {% endif %}
        </td>
      </tr>
    {% endfor %}
  </table>
</div>
