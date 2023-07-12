<script>
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import IconButton from '@smui/icon-button';
	import Textfield from '@smui/textfield';
	import CircularProgress from '@smui/circular-progress';
	import Button from '@smui/button';

	let question = '';
	let answer = '';
	let isLoading = false;

	async function getAnswer() {
		isLoading = true;
		const res = await fetch(`http://127.0.0.1:8000/ask/${question}`);
		const data = await res.json();

		answer = data.answer;
		isLoading = false;
	}

	function clear() {
		question = '';
		answer = '';
		isLoading = false;
	}
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h1>
		<span class="welcome">
			<picture>
				<source srcset={welcome} type="image/webp" />
				<img src={welcome_fallback} alt="Welcome" />
			</picture>
		</span>
	</h1>
	<div class="question">
		<Textfield bind:value={question} style="width: 75%;" label="Make a question..." />

		{#if !isLoading}
			<IconButton class="material-icons" on:click={getAnswer}>send</IconButton>
		{:else}
			<CircularProgress style="height: 32px; width: 32px;" indeterminate />
		{/if}
	</div>

	<div class="answer">
		<Textfield
			textarea
			bind:value={answer}
			input$resizable={true}
			style="width: 80%;"
			input$readonly
		/>
	</div>

	<div class="clear">
		<Button variant="raised" on:click={clear}>Clear</Button>
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}

	.question {
		width: 100%;
		height: 100%;
		margin-left: 20%;
		justify-content: center;
		margin-bottom: 15px;
	}

	.answer {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.clear {
		align-items: flex-start;
		margin-top: 10px;
	}
</style>
