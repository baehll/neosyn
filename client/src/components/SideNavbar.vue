<template> 
    <SidebarMenu :menu="menu" :collapsed="true"></SidebarMenu>
</template>

<script setup>
const menu = [
    {
        header: "Main Navigation",
        hiddenOnCollapse: true
    },{
        href: '/dashboard',
        title: 'Dashboard',
        icon: "fa-solid fa-chart-line"/*,
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
                href: '/metrics/content',
                title: 'Content'
            }
        ]*/
    },{
        href: "/interactions",
        title: "Interactions",
        icon: "fas fa-comments"
    },{
        href: "/",
        title: "Tasks",
        icon: "fas fa-check",
        disabled: true
    },{
        href: "/",
        title: "Search",
        icon: "fas fa-magnifying-glass",
        disabled: true
    },{
        href: "/",
        title: "Links",
        icon: "fas fa-link",
        disabled: true
    },{
        href: "/",
        title: "Statistics",
        icon: "fas fa-chart-simple",
        disabled: true
    }
]

</script>