<script>
    let input = 'Once upon a time.';
    let uppercase = 'ONCE UPON A TIME.';
    let lowercase = 'once upon a time.';
    let slug = 'once-upon-a-time';

    function copyToClipboard(id) {
        let copyText = document.getElementById(id);
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
    }

    function slugify(e) {
        let str = input.replace(/^\s+|\s+$/g, '');

        uppercase = str.toUpperCase();
        lowercase = str.toLowerCase();
        str = lowercase;

        var from = "ÁÄÂÀÃÅČÇĆĎÉĚËÈÊẼĔȆÍÌÎÏŇÑÓÖÒÔÕØŘŔŠŤÚŮÜÙÛÝŸŽáäâàãåčçćďéěëèêẽĕȇíìîïňñóöòôõøðřŕšťúůüùûýÿžþÞĐđßÆa·/_,:;";
        var to   = "AAAAAACCCDEEEEEEEEIIIINNOOOOOORRSTUUUUUYYZaaaaaacccdeeeeeeeeiiiinnooooooorrstuuuuuyyzbBDdBAa------";
        for (var i=0, l=from.length ; i<l ; i++) {
            str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
        }

        str = str.replace(/[^a-z0-9 -]/g, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-');

        slug = str;
    }
</script>

<main>
    <h1>Slugify</h1>
    <p>
        <label>Input:<br />
            <input type="text" name="input" bind:value={input}>
        </label>
    </p>
    <button on:click={slugify}>Slugify</button>
    <p>
        <label>Uppercase:<br />
            <input type="text" id="uppercase" name="uppercase" value={uppercase} readonly>
            <button on:click={() => copyToClipboard("uppercase")}>Copy</button>
        </label>
    </p>
    <p>
        <label>Lowercase:<br />
            <input type="text" id="lowercase" name="lowercase" value={lowercase} readonly>
            <button on:click={() => copyToClipboard("lowercase")}>Copy</button>
        </label>
    </p>
    <p>
        <label>Slug:<br />
            <input type="text" id="slug" name="slug" value={slug} readOnly>
            <button on:click={() => copyToClipboard("slug")}>Copy</button>
        </label>
    </p>
</main>

<style>
</style>
