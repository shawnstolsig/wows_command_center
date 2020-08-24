// package imports
import React from 'react'
import { makeStyles } from '@material-ui/core/styles';
import {
  AppBar,
  Button,
  IconButton,
  Toolbar,
  Typography,
  Link
} from '@material-ui/core'
import {
  Menu as MenuIcon
} from '@material-ui/icons'
import { connect } from 'react-redux'
import { Link as RouterLink } from 'react-router-dom'

// project imports
import { handleLogoutUser } from '../actions/authedUser'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}))

function Nav({ dispatch, authedUser }) {
  const classes = useStyles()

  const handleLogout = () => {
    dispatch(handleLogoutUser())
  }

  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" className={classes.title}>
          <Link component={RouterLink} to="/" color="inherit" underline="none">
            WoWs Command Center
          </Link>
        </Typography>

        {authedUser
          ? <Button color="inherit" onClick={handleLogout}>Logout</Button>
          : <Button color="inherit" component={RouterLink} to={'/login'}>Login</Button>
        }

      </Toolbar>
    </AppBar>
  )
}

function mapStateToProps(state) {
  return {
    authedUser: state.authedUser
  }
}

export default connect(mapStateToProps)(Nav)