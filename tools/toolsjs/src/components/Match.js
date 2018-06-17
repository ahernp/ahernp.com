import React from 'react';

export default class Match extends React.Component {
    constructor() {
        super();
        this.state = {
            input: 'Record3\nRecord4\nRecord4\nRecord1',
            keys: 'Record4\nRecord1',
            exclude: false,
            output: 'Record4\nRecord4\nRecord1'
        };
        this.onChange = this.onChange.bind(this);
    }

    onChange = (e) => {
        let { input, keys, exclude } = this.state;

        if (e.target.name === 'input')
            input = e.target.value;
        else if (e.target.name === 'keys')
            keys = e.target.value;
        else
            exclude = !exclude;

        const inputRecords = input.split('\n');
        const keyRecords = keys.split('\n');
        let output = '';
        for (let i = 0; i < inputRecords.length; i++) {
            let matchFound = false;
            for (let j = 0; j < keyRecords.length; j++) {
                if (inputRecords[i].indexOf(keyRecords[j]) > -1) {
                    matchFound = true;
                    break;
                }
            }
            if ((!matchFound && exclude) || (matchFound && !exclude))
                output = output + inputRecords[i] + '\n';
        }
        this.setState({ ...this.state, input, keys, exclude, output });
    };

    render() {
        const { input, keys, exclude, output } = this.state;
        return (
            <React.Fragment>
                <h1>Match Records</h1>
                <p>Keep or exclude matching records.</p>
                <p>
                    <label>Input:<br />
                        <textarea rows="4" cols="56" name="input" value={input} onChange={this.onChange}></textarea>
                    </label>
                </p>
                <p>
                    <label>Keys:<br />
                        <textarea rows="4" cols="56" name="keys" value={keys} onChange={this.onChange}></textarea>
                    </label>
                </p>
                <p>
                    <input type="checkbox" name="exclude" value={exclude} onChange={this.onChange} />
                    Exclude matches
                </p>
                <p>
                    <label>Output:<br />
                        <textarea rows="4" cols="56" value={output} readOnly></textarea>
                    </label>
                </p>
            </React.Fragment>
        );
    }
}