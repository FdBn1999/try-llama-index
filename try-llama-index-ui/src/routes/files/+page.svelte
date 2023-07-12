<script lang="ts">
	import DataTable, { Head, Body, Row, Cell } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import { onMount } from 'svelte';
	import LinearProgress from '@smui/linear-progress';
	import Snackbar, { Label, Actions } from '@smui/snackbar';
	import CircularProgress from '@smui/circular-progress';
	import Textfield from '@smui/textfield';

	type File = {
		_id: string;
		name: string;
		createdAt: Date;
	};

	let files: File[] = [];

	let filesLoaded = true;

	let snackbar: Snackbar;
	let snackbarMessage: string;
	let snackbarSuccess = true;

	let filesToUpload: any[] = [];

	let uploadingFile = false;

	onMount(async () => {
		getFiles();
	});

	async function getFiles() {
		filesLoaded = false;
		const res = await fetch(`http://127.0.0.1:8000/getallfiles`);
		const data = await res.json();

		const allFiles = JSON.parse(data);

		files = allFiles.map((f: any) => {
			const mappedFile: File = {
				_id: f._id,
				createdAt: f.createdAt,
				name: f.name
			};

			return mappedFile;
		});

		filesLoaded = true;
	}

	async function deleteFile(_id: string) {
		const res = await fetch(`http://127.0.0.1:8000/deletefile/${_id}`, {
			method: 'DELETE'
		});

		await showSnackbarByResponse(res);

		getFiles();
	}

	async function uploadFile() {
		uploadingFile = true;
		const fileToSend = filesToUpload[0];
		const formData = new FormData();

		formData.append('file', fileToSend);

		const res = await fetch('http://127.0.0.1:8000/uploadfile', {
			method: 'POST',
			body: formData
		});

		await showSnackbarByResponse(res);
		getFiles();

		filesToUpload = [];
		uploadingFile = false;
	}

	async function showSnackbarByResponse(res: Response) {
		snackbar.close();

		const data = await res.json();
		snackbarMessage = data.message;
		snackbarSuccess = res.ok;

		snackbar.open();
	}
</script>

<svelte:head>
	<title>Files</title>
	<meta name="description" content="Added files" />
</svelte:head>

<h1>Added files</h1>
<div class="hide-file-ui" style="margin-bottom: 10px;">
	<Textfield bind:files={filesToUpload} label="File to upload" type="file" />
	{#if !uploadingFile && filesToUpload?.length}
		<IconButton class="material-icons" on:click={uploadFile}>upload</IconButton>
	{:else if filesToUpload?.length}
		<CircularProgress style="height: 32px; width: 32px;" indeterminate />
	{/if}
</div>

<DataTable
	table$aria-label="File list"
	style="width: 100%; background: none;"
	container$class="container"
>
	<Head style="background: none;">
		<Row style="background: none;">
			<Cell style="background: none;">Id</Cell>
			<Cell style="width: 70%; background: none;">Name</Cell>
			<Cell style="background: none;">Created At</Cell>
			<Cell style="background: none">Actions</Cell>
		</Row>
	</Head>
	<Body style="background: none;">
		{#each files as item (item._id)}
			<Row>
				<Cell>{item._id}</Cell>
				<Cell>{item.name}</Cell>
				<Cell>{item.createdAt}</Cell>
				<Cell
					><IconButton class="material-icons" on:click={() => deleteFile(item._id)}
						>delete</IconButton
					></Cell
				>
			</Row>
		{/each}
	</Body>

	<LinearProgress
		indeterminate
		bind:closed={filesLoaded}
		aria-label="Data is being loaded..."
		slot="progress"
	/>

	<Snackbar bind:this={snackbar} class={snackbarSuccess ? 'demo-success' : 'demo-error'}>
		<Label>{snackbarMessage}</Label>
		<Actions>
			<IconButton class="material-icons" title="Dismiss">close</IconButton>
		</Actions>
	</Snackbar>
</DataTable>

<style>
	.hide-file-ui :global(input[type='file']::file-selector-button) {
		display: none;
	}

	.hide-file-ui :global(:not(.mdc-text-field--label-floating) input[type='file']) {
		color: transparent;
	}
</style>
