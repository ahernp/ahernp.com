<script>
    let input = 'Record3\nRecord4\nRecord4\nRecord1';
    const placeholder = 'Record1\nRecord3\nRecord4';

    $: output = deduplicate(input);

    function deduplicate() {
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
        return output;
    }
</script>

<main>
    <h1>Sort and Deduplicate</h1>
    <p>Sort and remove duplicates from a list:</p>
    <p>
        <label>Input:<br />
            <textarea rows="4" cols="56" bind:value={input}></textarea>
        </label>
    </p>
    <p>
        <label>Output:<br />
            <textarea rows="4" cols="56" value={output} readOnly placeholder={placeholder}></textarea>
        </label>
    </p>
</main>

<style>
</style>
