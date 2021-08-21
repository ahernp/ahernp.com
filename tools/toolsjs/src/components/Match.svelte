<script>
    import { copyToClipboard } from '../utils';
    let input = 'Record3\nRecord4\nRecord4\nRecord1',
        keys = 'Record4\nRecord1',
        exclude = false;
    const placeholder = 'Record4\nRecord4\nRecord1';

    $: output = deduplicate(input, keys, exclude);

    function deduplicate(input, keys, exclude) {
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
        return output;
    }
</script>

<main>
    <h1>Match Records</h1>
    <p>Keep or exclude matching records.</p>
    <p>
        <label>Input:<br />
            <textarea rows="4" cols="56" name="input" bind:value={input}></textarea>
        </label>
    </p>
    <p>
        <label>Keys:<br />
            <textarea rows="4" cols="56" name="keys" bind:value={keys}></textarea>
        </label>
    </p>
    <p>
        <label>
            <input type="checkbox" name="exclude" bind:checked={exclude} />
            Exclude matches
        </label>
    </p>
    <p>
        <label>Output:<br />
            <textarea id="output" rows="4" cols="56" value={output} readOnly></textarea>
            <button on:click={() => copyToClipboard("output")}>Copy</button>
        </label>
    </p>
</main>

<style>
</style>
