<script>
	import router from "page";
	import Cardgen from './components/Cardgen.svelte';
	import Compare from './components/Compare.svelte';
	import Deduplicate from './components/Deduplicate.svelte';
	import Match from './components/Match.svelte';
	import Slugify from './components/Slugify.svelte';

	const routePrefix = '/tools';
	const cardgenRoute = `${routePrefix}/cardgen`;
	const compareRoute = `${routePrefix}/compare`;
	const deduplicateRoute = `${routePrefix}/deduplicate`;
	const matchRoute = `${routePrefix}/match`;
	const slugifyRoute = `${routePrefix}/slugify`;
	let page;

	router(routePrefix, () => page = Cardgen);
	router(cardgenRoute, () => page = Cardgen);
	router(compareRoute, () => page = Compare);
	router(deduplicateRoute, () => page = Deduplicate);
	router(matchRoute, () => page = Match);
	router(slugifyRoute, () => page = Slugify);

	router.start();
</script>


<main>
	<p>
		<a href="{cardgenRoute}">Cardgen</a>
		<a href="{compareRoute}">Compare</a>
		<a href={deduplicateRoute}>Deduplicate</a>
		<a href={matchRoute}>Match</a>
		<a href={slugifyRoute}>Slugify</a>
    </p>
</main>

<svelte:component this={page} />

<style>
</style>
