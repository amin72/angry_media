import React, { Fragment } from 'react'
import './App.css'

import Posts from './components/posts/Posts'
import Header from './components/layout/header/Header'

const App = () => {
  return (
    <Fragment>
      <Header />
      <Posts />
    </Fragment>
  )
}

export default App