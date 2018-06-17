import React from 'react';
import { Link } from 'react-router-dom';

import Cardgen from '../components/Cardgen';
import Compare from '../components/Compare';
import Deduplicate from '../components/Deduplicate';
import Match from '../components/Match';


export default class Tools extends React.Component {
    render() {
        let tool = <Cardgen />;
        console.log(this.props.match.params.tool);
        switch(this.props.match.params.tool) {
            case 'compare': {
                tool = <Compare />;
                break;
            }
            case 'deduplicate': {
                tool = <Deduplicate />;
                break;
            }
            case 'match': {
                tool = <Match />;
                break;
            }
            default: {}
        }
        return (
            <React.Fragment>
                <p><Link to="/tools/cardgen">Cardgen</Link> <Link to="/tools/compare">Compare</Link> <Link to="/tools/deduplicate">Deduplicate</Link> <Link to="/tools/match">Match</Link></p>
                {tool}
            </React.Fragment>
        );
    }
}
