import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'

import moment from "moment-jalaali"
import fa from "moment/locale/fa"
moment.locale("fa", fa)

ReactDOM.render(
    <App />,
  document.getElementById('root')
)