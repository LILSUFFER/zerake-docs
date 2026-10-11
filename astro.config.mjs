// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://docs.zerake.com',
	integrations: [
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
				{ tag: 'script', attrs: { src: '/zk-diagrams.js', defer: true } },
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
				{ label: 'Движение средств', items: [
					{ label: 'Карта и обзор', slug: 'money/overview' },
					{ label: 'Адреса клуба', slug: 'money/addresses' },
					{ label: 'Пополнение', collapsed: false, items: [
						{ label: 'Заявки (TRC20, BEP20)', slug: 'money/deposit-request' },
						{ label: 'Персональные адреса (TON)', slug: 'money/deposit-personal' },
						{ label: 'Поиск платежей', slug: 'money/detection' },
					] },
					{ label: 'Снятие', collapsed: false, items: [
						{ label: 'Снятие и выплата', slug: 'money/withdrawal' },
						{ label: 'Откуда идёт выплата', slug: 'money/payout-sources' },
					] },
					{ label: 'Комиссии', slug: 'money/fees' },
					{ label: 'Курс GRAM', slug: 'money/gram-rate' },
					{ label: 'Лимиты и проверки', slug: 'money/limits' },
					{ label: 'Спорные платежи', slug: 'money/problems' },
				] },
				{ label: 'Игрокам', items: [
					{ label: 'Аккаунт', collapsed: true, items: [
						{ label: 'GG ID', slug: 'account/clubgg-id' },
						{ label: 'Кошелёк для выплат', slug: 'account/payout-wallet' },
						{ label: 'Секретная фраза', slug: 'account/secret-phrase' },
						{ label: 'PIN-код и Face ID', slug: 'account/pin' },
						{ label: 'Смена кошелька и восстановление', slug: 'account/recovery' },
					] },
					{ label: 'Столы', collapsed: true, items: [
						{ label: 'Уровни столов', slug: 'tables/levels' },
						{ label: 'Bad Beat Jackpot', slug: 'tables/jackpot' },
						{ label: 'Честная игра', slug: 'tables/fair-play' },
					] },
					{ label: 'Номера операций', slug: 'reference/operations' },
					{ label: 'Уведомления', slug: 'reference/notifications' },
				] },
				{ label: 'Безопасность', items: [
					{ label: 'Как мы защищаем деньги', slug: 'security/model' },
					{ label: 'Как защитить себя', slug: 'security/player' },
				] },
				{ label: 'Устройство системы', items: [
					{ label: 'Обзор архитектуры', slug: 'architecture/overview' },
					{ label: 'Выдача фишек', slug: 'architecture/chips' },
					{ label: 'Боты Telegram', slug: 'architecture/bots' },
					{ label: 'Журнал операций', slug: 'architecture/audit-log' },
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
