import React from 'react';

export default class Deduplicate extends React.Component {
    constructor() {
        super();
        this.state = {
            input: 'Record3\nRecord4\nRecord4\nRecord1',
            output: 'Record1\nRecord3\nRecord4'
        };
        this.changeInput = this.changeInput.bind(this);
    }

    changeInput(e) {
        const input = e.target.value;
        const inputRecords = input.split('\n').sort();
        let output = '';
        for (let i = 0; i < inputRecords.length - 1; i++) {
            if (inputRecords[i] !== inputRecords[i + 1])
                output = output + inputRecords[i] + '\n';
        }
        if (inputRecords.length === 0 || inputRecords.length === 1)
            output = inputRecords[0];
        else
            output = output + inputRecords[inputRecords.length - 1] + '\n';

        this.setState({ ...this.state, input, output });
    }

    render() {
        const { input, output } = this.state;
        return (
            <React.Fragment>
                <h1>Sort and Deduplicate</h1>
                <p>Sort and remove duplicates from a list:</p>
                <p>
                    <label>Input:<br />
                        <textarea rows="4" cols="56" value={input} onChange={this.changeInput}></textarea>
                    </label>
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