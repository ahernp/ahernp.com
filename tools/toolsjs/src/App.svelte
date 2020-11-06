<script>
	import router from "page";
	import Cardgen from './components/Cardgen.svelte';
	import Compare from './components/Compare.svelte';
	import Deduplicate from './components/Deduplicate.svelte';
	import Match from './components/Match.svelte';

	const routePrefix = '/tools';
	const cardgenRoute = `${routePrefix}/cardgen`;
	const compareRoute = `${routePrefix}/compare`;
	const deduplicateRoute = `${routePrefix}/deduplicate`;
	const matchRoute = `${routePrefix}/match`;
	let page;

	router(routePrefix, () => page = Cardgen);
	router(cardgenRoute, () => page = Cardgen);
	router(compareRoute, () => page = Compare);
	router(deduplicateRoute, () => page = Deduplicate);
	router(matchRoute, () => page = Match);

	router.start();
</script>


<main>
	<p>
		<a href="{cardgenRoute}">Cardgen</a>
		<a href="{compareRoute}">Compare</a>
		<a href={deduplicateRoute}>Deduplicate</a>
		<a href={matchRoute}>Match</a>
    </p>
</main>

<svelte:component this={page} />

<style>
</style>
