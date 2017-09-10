# SkillScout - Website README #

## Overview ##

This started as the framework from generator-react-webpack (https://github.com/react-webpack-generators/generator-react-webpack)

The UI process is as follows:
1. User enters a city Location (error message is provided when location can not be found)
2. If a valid city/location was given, the google maps geocode API is used to determine the city/locations's place ID and that place ID is used to look up relevant data from a firebase database, that has been populated with values from a combined NLP and webscraping algorithm (see the /backend folder README)
3. That endpoint data is rendered in various lists and charts

## Current File Structure of Source (Folder `/src`) ##

(generated with bash command `tree src`)

```
src
├── actions
│   └── README.md
├── components
│   ├── Main.js
│   ├── background
│   │   └── Background.js
│   ├── charts
│   │   ├── DoughnutChart.js
│   │   ├── LongTrendsChart.js
│   │   └── RecentTrendsChart.js
│   ├── cityList
│   │   └── CityList.js
│   ├── container
│   │   └── Container.js
│   ├── footer
│   │   └── Footer.js
│   ├── input
│   │   └── InputAndButton.js
│   ├── inputGuide
│   │   └── InputGuide.js
│   ├── logo
│   │   └── Logo.js
│   ├── popups
│   │   └── SearchErrorPopupContent.js
│   └── results
│       ├── JobsDropdown.js
│       └── Results.js
├── config
│   ├── README.md
│   ├── base.js
│   ├── dev.js
│   ├── dist.js
│   └── test.js
├── data
│   └── cityTableData.js
├── favicon.ico
├── images
├── index.html
├── index.js
├── sources
│   └── README.md
├── stores
│   └── README.md
├── styles
│   ├── App.css
│   └── App_copy.css
└── styles-scss
    ├── App.scss
    ├── _Background.scss
    ├── _Container.scss
    ├── _Footer.scss
    ├── _Input.scss
    ├── _Logo.scss
    ├── _Results.scss
    ├── _SubmitButton.scss
    └── _include-media.scss
```
