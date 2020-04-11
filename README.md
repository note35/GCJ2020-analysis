# Google Code Jam 2020 post analysis

- This work provides interactive way to analyze the GCJ2020's result, if you just want to see processed result, [vstrimaitis/google_codejam_stats](https://github.com/vstrimaitis/google_codejam_stats) provides [the site](https://vstrimaitis.github.io/google_codejam_stats/) with much better interface.
- See **analysis_{round}.ipynb** for the result
- See directory crawler for the detail how to get data

## Development

### Crawler

All scripts can be executed by native python interpreter in Linux/MacOS with python3.6 or above.

### Analysis

```bash
$ pipenv install
$ pipenv shell
$ jupyter notebook
```

Then you can access `http://localhost:8888` to analyze the data.

## Cleanup

```bash
$ pipenv uninstall --all
```
