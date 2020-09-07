// package imports
import React from 'react'
import {
  Box,
  Container,
  Grid,
  Button,
  Typography
} from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'
import queryStrings from 'query-string'

// project imports
import wgLogo from '../assets/wg_logo.png'

const useStyles = makeStyles((theme) => ({
  regionButton: {
    margin: theme.spacing(1),
  },
  wgLogo: {
    maxHeight: 50
  },

}))

export default function Login({ location }) {
  const classes = useStyles()

  // get any error messages from query strings
  const params = queryStrings.parse(location.search)

  // a function for helping build the URL based on region
  const buildURL = (region) => {

    // get the app id from .env (this isn't necessarily a secret)
    const appID = process.env.REACT_APP_WOWS_APP_ID

    // specify where WG should send the user back to
    const redirectURL = `${process.env.REACT_APP_API_URL}openid`

    // get the domain based on the region
    let domain
    if (region === 'NA') domain = 'com';
    else if (region === 'EU') domain = 'eu';
    else if (region === 'RU') domain = 'ru';
    else if (region === 'ASIA') domain = 'asia';

    // return constructed URL
    return `https://api.worldoftanks.${domain}/wot/auth/login/?application_id=${appID}&redirect_uri=${encodeURIComponent(redirectURL)}`
  }

  return (
    <Container className={classes.container}>
      <Typography variant="h6" align="center">Please select your region to login with WG credentials.</Typography>
      <Box align="center">
        <img src={wgLogo} className={classes.wgLogo} alt=''/>
      </Box>
      <Grid container spacing={2} align="center">
        <Grid item xs={12}>
          <Button color="primary" href={buildURL('NA')} variant="contained" className={classes.regionButton}>NA</Button>
          <Button color="primary" href={buildURL('EU')} variant="contained" className={classes.regionButton}>EU</Button>
          <Button color="primary" href={buildURL('RU')} variant="contained" className={classes.regionButton}>RU</Button>
          <Button color="primary" href={buildURL('ASIA')} variant="contained" className={classes.regionButton}>ASIA</Button>
        </Grid>
      </Grid>
      {params.error && <Typography variant="body1" color='error'>Error logging in, please try again.</Typography>}

    </Container>
  )
}