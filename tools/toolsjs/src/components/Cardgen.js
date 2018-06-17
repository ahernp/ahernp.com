import React from 'react';

export default class Cardgen extends React.Component {
    constructor() {
        super();
        this.state = {
            data: '#Name,#URL,#Description\nGoogle,www.google.com,Search engine.\nAmazon,www.amazon.co.uk,Bookshop.',
            delimiter: ',',
            template: '<li>#Name <a href="https://#URL" title="#Description"> #URL</a> #Description</li>',
            output: '<li>Google <a href="https://www.google.com" title="Search engine."> www.google.com</a> Search engine.</li>\n<li>Amazon <a href="https://www.amazon.co.uk" title="Bookshop."> www.amazon.co.uk</a> Bookshop.</li>'
        };
        this.onChange = this.onChange.bind(this);
    }

    onChange(e) {
        this.setState({ ...this.state, [e.target.name]: e.target.value });
    }

    generateCards() {
        const { data, delimiter, template } = this.state;

        const dataRecords = data.split('\n');
        const labels = dataRecords[0].split(delimiter);
        let outputString: string = '';
        for (let i = 1; i < dataRecords.length; i++) {
            let currentCard = template;
            const currentData = dataRecords[i].split(delimiter);
            for (let j = 0; j < currentData.length; j++) {
                let currentLabel = new RegExp(labels[j], 'g');
                currentCard = currentCard.replace(currentLabel, currentData[j]);
            }
            outputString = outputString + currentCard + "\n";
        }

        this.setState({ ...this.state, output: outputString });
    }

    render() {
        const { data, delimiter, template, output } = this.state;
        return (
            <React.Fragment>
                <h1>Generate Card Output</h1>
                <p>
                    Generate multiple cards from a single template by replacing
                    label/references with equivalent data.
                </p>
                <p>
                    <label>Data:<br />
                        <textarea rows="4" cols="56" name="data" value={data} onChange={this.onChange}></textarea>
                    </label>
                </p>
                <p>Delimiter used in data: <input type="text" size="1" name="delimiter" value={delimiter} onChange={this.onChange} /></p>
                <p>
                    <label>Template:<br />
                        <textarea rows="4" cols="56" value={template} name="template" onChange={this.onChange}></textarea>
                    </label>
                </p>
                <button onClick={this.generateCards.bind(this)}>Generate Cards</button>
                <p>
                    <label>Output:<br />
                        <textarea rows="4" cols="56" value={output} readOnly></textarea>
                    </label>
                </p>
            </React.Fragment>
        );
    }
}