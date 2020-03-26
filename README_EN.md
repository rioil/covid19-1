# Shiga COVID-19 Task Force website

![](https://github.com/shiga-pref-org/covid19/workflows/production%20deploy/badge.svg)

![](https://github.com/shiga-pref-org/covid19/workflows/development%20deploy/badge.svg)


[![Netlify Status](https://api.netlify.com/api/v1/badges/9a8952b2-4514-4dd1-88e6-751c364b3df7/deploy-status)]((https://app.netlify.com/sites/happy-roentgen-86f936/deploys))


[![Shiga COVID-19 Task Force website](https://github.com/Shiga-pref-org/covid19/raw/development/static/ogp.png)](https://stopcovid19.metro.tokyo.lg.jp/)


### [日本語](./README.md) | [English](./README_EN.md) |

### BEWARE THAT THIS DOCUMENT MAY INCORRECT AT THIS MOMENT. JAPANESE VERSION IS PRIOR THAN ANY OTHER VERSION.

## How to Contribute

All contributions are welcome!
Please check [How to contribute](./.github/CONTRIBUTING_EN.md) for details.

## Code of Conduct

Please check [Code of conduct for developers](./.github/CODE_OF_CONDUCT_EN.md) for details.

## License
This software is released under [the MIT License](./LICENSE.txt).

##　Shiga version specific infomation

### Our development direction
- Earlier first release is our first proority. Therefore,we won't work on internationalization before the website rereased in stable.
- Due to the same reason above,flow feature is also disabled.
- To re:enable those feature quickly, we just remobe those features from UIs,keeping other codes out of UI. 

## For Developers

### How to Set Up Environments

- Required Node.js version: 10.19.0 or higher

**Use yarn**
```bash
# install dependencies
$ yarn install

# serve with hot reload at localhost:3000
$ yarn dev
```

**Use docker**
```bash
# serve with hot reload at localhost:3000
$ docker-compose up --build
```

### How to resolve `Cannot find module ****` error

**Use yarn**
```bash
$ yarn install
```

**Use docker**
```bash
$ docker-compose run --rm app yarn install
```

### Detect procition/others environment

On the production environment, `'production'` is assigned to `process.env.GENERATE_ENV` variable, on the other case `'development'` is assigned to the variable.
Please use the variable to detect which enviroinment is used at the runtime.

### Deployment to Staging & Production Environments

<del>When `master` branch is updated, the HTML files will be automatically built onto `production` branch,
and then the production site (https://stopcovid19.pref.shiga.jp/) will be also updated.

When `development` branch is updated, the HTML files will be automatically built onto `dev-pages` branch,
and then the development site (https://frosty-lamarr-66d313.netlify.com/) will be also updated.</del>
