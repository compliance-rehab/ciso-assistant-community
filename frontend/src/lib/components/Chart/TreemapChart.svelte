<script lang="ts">
	import { onMount } from 'svelte';
	import { m } from '$paraglide/messages';
	import { safeTranslate } from '$lib/utils/i18n';

	interface treeType {
		name: string;
		id: string;
		children: any[];
	}
	interface Props {
		width?: string;
		height?: string;
		classesContainer?: string;
		title?: string;
		name?: string;
		tree: treeType[];
	}

	let {
		width = 'w-auto',
		height = 'h-full',
		classesContainer = '',
		title = '',
		name = '',
		tree
	}: Props = $props();

	tree = tree.map((item) => ({
		...item,
		name: safeTranslate(item.id),
		children: item.children?.map((child) => ({
			...child,
			name: safeTranslate(child.id)
		}))
	}));

	const chart_id = `${name}_div`;
	onMount(async () => {
		if (tree?.length > 0) {
			const echarts = await import('echarts');
			let chart = echarts.init(document.getElementById(chart_id), null, { renderer: 'svg' });
			// specify chart configuration item and data

			var option = {
				toolbox: {
					show: true,
					feature: {
						restore: { show: true }
					}
				},
				title: {
					subtext: title
				},
				tooltip: {
					trigger: 'item',
					formatter: '{b}/data: {c}'
				},
				series: {
					type: 'treemap',
					breadcrumb: {
						show: false
					},
					// type: 'sunburst',
					// emphasis: {
					//     focus: 'ancestor'
					// },
					//upperLabel: {
					//	show: true
					//},
					leafDepth: 1,
					roam: false,
					visibleMin: 1,
					colorSaturation: [0.3, 0.4],
					data: tree,
					radius: [30, '95%'],
					sort: undefined,
					itemStyle: {
						borderRadius: 7,
						borderWidth: 2
					}
				}
			};

			// console.debug(option);

			// use configuration item and data specified to show chart
			chart.setOption(option);

			window.addEventListener('resize', function () {
				chart.resize();
			});
		}
	});
</script>

{#if tree.length === 0}
	<div class="flex flex-col justify-center items-center h-full">
		<span class="text-center text-gray-600">{m.noDataAvailable()}</span>
	</div>
{:else}
	<div id={chart_id} class="{width} {height} {classesContainer}"></div>
{/if}
