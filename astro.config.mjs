// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';

// https://astro.build/config
export default defineConfig({
	site: 'https://docs.zerake.com',
	integrations: [
		mermaid({ theme: 'default', autoTheme: true }),
		starlight({
			title: 'Zerake Docs',
			description: 'Документация клуба Zerake: аккаунт, пополнение и снятие фишек, сети, безопасность и устройство системы.',
			defaultLocale: 'root',
			locales: { root: { label: 'Русский', lang: 'ru' } },
			logo: { light: './src/assets/logo-light.svg', dark: './src/assets/logo-dark.svg', replacesTitle: true },
			favicon: '/favicon.svg',
			customCss: ['./src/styles/theme.css'],
			components: { PageTitle: './src/components/PageTitle.astro', SiteTitle: './src/components/SiteTitle.astro' },
			head: [
				{ tag: 'link', attrs: { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap' } },
				// light by default, like Cloudflare's docs; the switch in the header still works
				{ tag: 'script', content: "try{if(!localStorage.getItem('starlight-theme')){localStorage.setItem('starlight-theme','light');document.documentElement.dataset.theme='light'}}catch(e){}" },
			],
			lastUpdated: true,
			pagination: true,
			social: [{ icon: 'telegram', label: 'Telegram', href: 'https://t.me/zerakebot' }],
			sidebar: [
				{ label: 'Начало', items: [
					{ label: 'Обзор', link: '/' },
					{ label: 'Быстрый старт', slug: 'start/quickstart' },
					{ label: 'Словарь', slug: 'start/glossary' },
					{ label: 'Вопросы и ответы', slug: 'faq' },
				] },
				{ label: 'Игрокам', items: [
					{ label: 'Аккаунт', collapsed: true, items: [
						{ label: 'ID в ClubGG', slug: 'account/clubgg-id' },
						{ label: 'Кошелёк для выплат', slug: 'account/payout-wallet' },
						{ label: 'Секретная фраза', slug: 'account/secret-phrase' },
						{ label: 'PIN-код и Face ID', slug: 'account/pin' },
						{ label: 'Смена кошелька и восстановление', slug: 'account/recovery' },
					] },
					{ label: 'Пополнение фишек', collapsed: true, items: [
						{ label: 'Как это работает', slug: 'top-up/how-it-works' },
						{ label: 'TRC20 и BEP20: заявка', slug: 'top-up/request' },
						{ label: 'TON и GRAM: личный адрес', slug: 'top-up/personal-address' },
						{ label: 'Статусы и проблемы', slug: 'top-up/statuses' },
					] },
					{ label: 'Снятие фишек', collapsed: true, items: [
						{ label: 'Как это работает', slug: 'cash-out/how-it-works' },
						{ label: 'Комиссии', slug: 'cash-out/fees' },
						{ label: 'Проверка платёжеспособности', slug: 'cash-out/solvency' },
						{ label: 'Статусы и проблемы', slug: 'cash-out/statuses' },
					] },
					{ label: 'Столы', collapsed: true, items: [
						{ label: 'Уровни столов', slug: 'tables/levels' },
						{ label: 'Bad Beat Jackpot', slug: 'tables/jackpot' },
						{ label: 'Честная игра', slug: 'tables/fair-play' },
					] },
				] },
				{ label: 'Справочник', items: [
					{ label: 'Сети, минимумы и лимиты', slug: 'reference/networks' },
					{ label: 'Номера операций', slug: 'reference/operations' },
					{ label: 'Уведомления', slug: 'reference/notifications' },
				] },
				{ label: 'Безопасность', items: [
					{ label: 'Как мы защищаем деньги', slug: 'security/model' },
					{ label: 'Как защитить себя', slug: 'security/player' },
				] },
				{ label: 'Устройство системы', items: [
					{ label: 'Архитектура', collapsed: true, items: [
						{ label: 'Обзор архитектуры', slug: 'architecture/overview' },
						{ label: 'Поток пополнения', slug: 'architecture/top-up-flow' },
						{ label: 'Поток выплаты', slug: 'architecture/payout-flow' },
						{ label: 'Хранение средств', slug: 'architecture/funds' },
						{ label: 'Выдача фишек', slug: 'architecture/chips' },
						{ label: 'Боты Telegram', slug: 'architecture/bots' },
						{ label: 'Журнал операций', slug: 'architecture/audit-log' },
					] },
				] },
				{ label: 'Команде', items: [
					{ label: 'Админка', slug: 'team/admin-panel' },
					{ label: 'Очередь заявок', slug: 'team/queue' },
					{ label: 'Поддержка игроков', slug: 'team/support' },
				] },
			],
		}),
	],
});
