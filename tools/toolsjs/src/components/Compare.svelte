<script>
    let input1 = 'Record1\nRecord3\nRecord4';
    let input2 = 'Record1\nRecord2\nRecord3';
    let output = 'Results: 2 matches; 1 inserts; 1 deletes.\nI:Record2\nD:Record4';

    function sortAndCompare() {
        const inputLines1 = input1.split('\n').sort();
        const inputLines2 = input2.split('\n').sort();

        let resultString = '',
            position1 = 0,
            position2 = 0,
            matchCount = 0,
            insertCount = 0,
            deleteCount = 0;

        while (position1 < inputLines1.length && position2 < inputLines2.length) {
            if (inputLines1[position1] > inputLines2[position2]) {
                resultString = resultString + "I:" + inputLines2[position2] + '\n';
                position2++; insertCount++;
            }
            else if (inputLines1[position1] < inputLines2[position2]) {
                resultString = resultString + "D:" + inputLines1[position1] + '\n';
                position1++; deleteCount++;
            }
            else {
                position1++; position2++; matchCount++;
            }
        }
        while (position1 < inputLines1.length) {
            resultString = resultString + "D:" + inputLines1[position1] + '\n';
            position1++; deleteCount++;
        }
        while (position2 < inputLines2.length) {
            resultString = resultString + "I:" + inputLines2[position2] + '\n';
            position2++; insertCount++;
        }
        output = `Results: ${matchCount} matches; ${insertCount} inserts; ${deleteCount} deletes.\n${resultString}`;
    }
</script>

<main>
    <h1>Compare two lists</h1>
    <p>Sort and compare inputs.</p>
    <p>
        <label>First Input:<br />
            <textarea rows="4" cols="56" name="input1" bind:value={input1}></textarea>
        </label>
    </p>
    <p>
        <label>Second Input:<br />
            <textarea rows="4" cols="56" name="input2" bind:value={input2}></textarea>
        </label>
    </p>
    <button on:click={sortAndCompare}>Sort &amp; Compare</button>
    <p>
        <label>Output:<br />
            <textarea rows="4" cols="56" value={output} readOnly></textarea>
        </label>
    </p>
    <p>If a line in First Input is missing from Second Input then it is included in Output with the prefix "D:".</p>
            <p>If a line in Second Input is missing from First Input then it is included in Output with the prefix "I:".</p>
</main>

<style>
</style>
