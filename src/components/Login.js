// package imports
import React from 'react'
import {
  Box,
  Button,
  Typography
} from '@material-ui/core'
import queryStrings from 'query-string'

// project imports

export default function Login({ location }) {

  // get any error messages from query strings
  const params = queryStrings.parse(location.search)

  // a function for helping build the URL based on region
  const buildURL = (region) => {

    // get the app id from .env (this isn't necessarily a secret)
    const appID = process.env.REACT_APP_WOWS_APP_ID
    
    // specify where WG should send the user back to
    const redirectURL = `http://localhost:3000/complete_login`

    // get the domain based on the region
    let domain
    if(region === 'NA') domain = 'com';
    else if(region === 'EU') domain = 'eu';
    else if(region === 'RU') domain = 'ru';
    else if(region === 'ASIA') domain = 'asia';

    // return constructed URL
    return `https://api.worldoftanks.${domain}/wot/auth/login/?application_id=${appID}&redirect_uri=${encodeURIComponent(redirectURL)}`
  }

  return (
    <Box>
      {params.error && <Typography variant="body1" color='error'>Error logging in, please try again.</Typography>}
      <Button color="inherit" href={buildURL('NA')}>NA</Button>
      <Button color="inherit" href={buildURL('EU')}>EU</Button>
      <Button color="inherit" href={buildURL('RU')}>RU</Button>
      <Button color="inherit" href={buildURL('ASIA')}>ASIA</Button>
    </Box>
  )
}