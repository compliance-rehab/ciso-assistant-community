<script lang="ts">
	import type { PageData } from './$types';
	import { page } from '$app/state';
	import SuperForm from '$lib/components/Forms/Form.svelte';
	import TextField from '$lib/components/Forms/TextField.svelte';
	import { SetPasswordSchema } from '$lib/utils/schemas';

	import { m } from '$paraglide/messages';
	import { zod } from 'sveltekit-superforms/adapters';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	function getUUID() {
		const matches = page.url.pathname.split('/');
		return matches ? matches[2] : null;
	}
</script>

<div class="flex w-full h-full items-center justify-center">
	<div class="flex flex-col bg-white p-12 w-2/5 rounded-lg shadow-lg items-center space-y-4">
		<div class="bg-primary-300 px-6 py-5 rounded-full text-3xl">
			<i class="fa-solid fa-key"></i>
		</div>
		<p class="text-gray-600 text-sm text-center">
			{m.youCanSetNewPassword()}.<br />
			{m.userWillBeDisconnected()}.
		</p>
		<!-- SuperForm with dataType 'form' -->
		<div class="flex w-full">
			<SuperForm
				class="flex flex-col space-y-3 w-full"
				data={data?.form}
				dataType="form"
				validators={zod(SetPasswordSchema)}
			>
				{#snippet children({ form })}
					<input class="input" type="hidden" name="user" value={getUUID()} />
					<TextField type="password" {form} field="new_password" label={m.newPassword()} />
					<TextField
						type="password"
						{form}
						field="confirm_new_password"
						label={m.confirmNewPassword()}
					/>
					<p class="pt-3">
						<button
							class="btn preset-filled-primary-500 font-semibold w-full"
							data-testid="save-button"
							type="submit">{m.setPassword()}</button
						>
					</p>
				{/snippet}
			</SuperForm>
		</div>
	</div>
</div>
