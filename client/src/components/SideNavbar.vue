<template> 
    <SidebarMenu :menu="menu" :collapsed="true"></SidebarMenu>
</template>

<script setup>
const menu = [
    {
        header: "Main Navigation",
        hiddenOnCollapse: true
    },{
        href: '/',
        title: 'Metrics',
        icon: "fa-solid fa-chart-line",
        child: [
            {
                href: '/metrics/dashboard',
                title: 'Dashboard'
            }, 
            {
                href: '/metrics/explore',
                title: 'Explore'
            }, 
            {
                href: '/metrics/inbox',
                title: 'Inbox'
            }, 
            {
                href: '/metrics/analyze',
                title: 'Analyze'
            }, 
            {
                href: '/metrics/share',
                title: 'Share'
            }, 
            {
                href: '/metrics/report',
                title: 'Report'
            }, 
            {
                href: 'metrics/content',
                title: 'Content'
            }
        ]
    },{
        href: "/",
        title: "Interactions",
        icon: "fas fa-comments"
    },{
        href: "/",
        title: "Tasks",
        icon: "fas fa-check"
    },{
        href: "/",
        title: "Search",
        icon: "fas fa-magnifying-glass"
    },{
        href: "/",
        title: "Links",
        icon: "fas fa-link"
    },{
        href: "/",
        title: "Statistics",
        icon: "fas fa-chart-simple"
    }
]

</script>