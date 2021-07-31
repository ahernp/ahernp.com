<script>
    import { copyToClipboard } from '../utils';
    let data = '#Name,#URL,#Description\nGoogle,www.google.com,Search engine.\nAmazon,www.amazon.co.uk,Bookshop.';
    let delimiter = ',';
    let template = '<li>#Name <a href="https://#URL" title="#Description"> #URL</a>#Description</li>';
    let output = '<li>Google <a href="https://www.google.com" title="Search engine."> www.google.com</a> Search engine.</li>\n<li>Amazon <a href="https://www.amazon.co.uk" title="Bookshop."> www.amazon.co.uk</a> Bookshop.</li>';

    function generateCards(e) {
        const dataRecords = data.split('\n');
        const labels = dataRecords[0].split(delimiter);
        let outputString = '';
        for (let i = 1; i < dataRecords.length; i++) {
            let currentCard = template;
            const currentData = dataRecords[i].split(delimiter);
            for (let j = 0; j < currentData.length; j++) {
                let currentLabel = new RegExp(labels[j], 'g');
                currentCard = currentCard.replace(currentLabel, currentData[j]);
            }
            outputString = outputString + currentCard + "\n";
        }
        output = outputString;
    }
</script>

<main>
    <h1>Generate Card Output</h1>
    <p>
        Generate multiple cards from a single template by replacing
        label/references with equivalent data.
    </p>
    <p>
        <label>Data:<br />
            <textarea rows="4" cols="56" name="data" bind:value={data}></textarea>
        </label>
    </p>
    <p>Delimiter used in data: <input type="text" size="1" name="delimiter" bind:value={delimiter}></p>
    <p>
        <label>Template:<br />
            <textarea rows="4" cols="56" bind:value={template} name="template"></textarea>
        </label>
    </p>
    <button on:click={generateCards}>Generate Cards</button>
    <p>
        <label>Output:<br />
            <textarea id="output" rows="4" cols="56" value={output} readOnly></textarea>
            <button on:click={() => copyToClipboard("output")}>Copy</button>
        </label>
    </p>
</main>

<style>
</style>
