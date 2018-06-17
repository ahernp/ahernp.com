import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import Tools from './smartcomponents/Tools';

class App extends Component {
    render() {
        return (
            <Router>
                <Switch>
                    <Route path='/tools/:tool?' component={Tools} />
                    <Route component={Tools} />
                </Switch>
            </Router>
        );
    }
}

export default App;
