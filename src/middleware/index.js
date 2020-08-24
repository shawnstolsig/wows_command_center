// package imports
import thunk from 'redux-thunk'
import { applyMiddleware, compose } from 'redux'

// project imports


// this is used for Chrome's Redux Dev Tools extension
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose

export default composeEnhancers(applyMiddleware(thunk))
