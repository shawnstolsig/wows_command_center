// library imports
import React from 'react';
import ReactDOM from 'react-dom';
import 'typeface-roboto';
import { CssBaseline } from '@material-ui/core'
import { createStore } from 'redux'
import { Provider } from 'react-redux'

// project imports
import './index.css';
import App from './App';
import reducers from './reducers'
import middleware from './middleware'
import * as serviceWorker from './serviceWorker';

// create the redux store
const store = createStore(reducers, middleware)

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <CssBaseline />
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
