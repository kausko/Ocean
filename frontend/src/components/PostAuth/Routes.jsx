import React from 'react'
import { Switch, Route, Redirect } from 'react-router-dom'
import Feed from './Feed/Feed'
import Communities from './Communities/Communities'
import CheerSquad from './CheerSquad/CheerSquad'

// eslint-disable-next-line import/no-anonymous-default-export
export default () => 
    <Switch>
        <Route path='/home/feed' component={Feed}/>
        <Route path='/home/communities' component={Communities}/>
        <Route path='/home/cheer' component={CheerSquad}/>
        <Redirect from='/home' to='/home/feed'/>
    </Switch>