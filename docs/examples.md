# Exemples

Quelques exemples avec Python ou JavaScript pour être inspiré pour votre code.
N'hésitez pas à ajouter votr propre exemple d'usage avec une pull-request!


## En utilisant Python

### Géocoder une seule valeur

```python
>>> import requests
>>> ADDOK_URL = 'http://api-adresse.data.gouv.fr/search/'
>>> response = requests.get(ADDOK_URL, params={'q': 'lill', 'limit': 5})
>>> response.json()
# => {'type': 'FeatureCollection', 'attribution': 'BAN',...
```


### Géocoder un fichier entier

```python
import requests

# Utillisez http://localhost:7878 si vous utilisez une instance locale.
ADDOK_URL = 'http://api-adresse.data.gouv.fr/search/csv/'


def geocode(filepath_in):
    with open(filepath_in, 'rb') as f:
        filename, response = post_to_addok(filepath_in, f.read())
        write_response_to_disk(filename, response)


def geocode_chunked(filepath_in, filename_pattern, chunk_by):
    with open(filepath_in, 'r') as bigfile:
        headers = bigfile.readline()
        current_lines = bigfile.readlines(chunk_by)
        i = 1
        while current_lines:
            current_filename = filename_pattern.format(i)
            current_csv = ''.join([headers] + current_lines)
            filename, response = post_to_addok(current_filename, current_csv)
            write_response_to_disk(filename, response)
            current_lines = bigfile.readlines(chunk_by)
            i += 1


def write_response_to_disk(filename, response, chunk_size=1024):
    with open(filename, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def post_to_addok(filename, filelike_object):
    files = {'data': (filename, filelike_object)}
    response = requests.post(ADDOK_URL, files=files)
    # You might want to use https://github.com/g2p/rfc6266
    content_disposition = response.headers['content-disposition']
    filename = content_disposition[len('attachment; filename="'):-len('"')]
    return filename, response


# Geocoder votre fichier en une fois s'il est petit.
geocode('data.csv')
# => data.geocoded.csv

# Sinon, geocoder-le par morceaux quand il est gros.
chunk_by = 50 * 2  # approximative number of lines.
geocode_chunked('data.csv', 'result-{}.csv', chunk_by)
# => result-1.geocoded.csv, result-2.geocoded.csv, etc
```


## En utilisant JavaScript (côté client)

```html
<!doctype html>
<meta charset=utf-8>
<title>Test addok + fetch</title>
<link rel="icon" href="data:;base64,iVBORw0KGgo=">
<script>
  /* Utillisez http://localhost:7878 si vous utilisez une instance locale. */
  const url = new URL('http://api-adresse.data.gouv.fr/search')
  const params = {q: 'lil'}
  Object.keys(params).forEach(
    key => url.searchParams.append(key, params[key])
  )
  fetch(url)
    .then(response => {
      if (response.status >= 200 && response.status < 300) {
        return response
      } else {
        const error = new Error(response.statusText)
        error.response = response
        throw error
      }
    })
    .then(response => response.json())
    .then(data => console.log('request succeeded with JSON response', data))
    .catch(error => console.log('request failed', error))
</script>
```


## En utilisant JavaScript (côté serveur)

```javascript
const fetch = require('node-fetch'); // npm install node-fetch
const FormData = require('form-data'); // npm install form-data
const fs = require('fs');

const form = new FormData();
      // Trouver annuaire-des-debits-de-tabac-deb.csv
      // at https://gist.github.com/ThomasG77/eaf00981be333a5a995cf87f3d6b3c78
      form.append('data', fs.createReadStream('./annuaire-des-debits-de-tabac-deb.csv'));
      form.append('columns', 'NUMERO ET LIBELLE DE VOIE');
      form.append('columns', 'COMMUNE');

fetch('http://api-adresse.data.gouv.fr/search/csv/', {
  method: 'POST', body: form
})
.then(res => res.text())
.then(text => {
  console.log(text);
});
```

Ou en utilisant [request-promise](https://www.npmjs.com/package/request-promise):

```javascript
const fs = require('fs');
const path = require('path')
// requires npm install request request-promise
const request = require('request-promise');

var formData = {
  columns: ['NUMERO ET LIBELLE DE VOIE', 'COMMUNE'],
  data: fs.createReadStream('./annuaire-des-debits-de-tabac-deb.csv')
};

request.post({
  url: 'http://api-adresse.data.gouv.fr/search/csv/',
  formData: formData
}).then(function (text) {
  // You might want to use fs.writeFile instead because writeFileSync
  // blocks the event loop. See section fs.writeFileSync() at
  // http://www.daveeddy.com/2013/03/26/synchronous-file-io-in-nodejs/
  fs.writeFileSync('./out.csv', text);
})
.catch(function (err) {
  console.log('request failed', error);
});
```
