$(document).ready(function() {
    $.ajax({
        url: '/get_menus/',
        type: 'GET',
        success: function(data) {
            $('.sidebar-menu').html('');
            var html = '';
            html += '<li class="header">MAIN NAVIGATION</li>';
            html += '<li class="active treeview">';
            html += '<a href="/">';  // "Dashboard" menu link
            html += '<i class="fa fa-dashboard"></i> <span>Dashboard</span>';
            html += '</a>';
            html += '</li>';
            var categoryMenuList = data.category_menu_list;
            $.each(categoryMenuList, function(index, item){
                html += '<li class="treeview">';
                html += '<a href="#">';
                html += '<i class="fa fa-table"></i> <span>'+item.category+'</span>';
                html += '<i class="fa fa-angle-left pull-right"></i>';
                html += '</a>';
                html += '<ul class="treeview-menu">';
                $.each(item.menus, function(index, item){
                    html += '<li><a href="'+item.url+'"><i class="fa fa-circle-o"></i>'+item.title+'</a></li>';
                });
                html += '</ul>';
                html += '</li>';
            });
            $('.sidebar-menu').append(html);

            // Add custom click event to toggle the submenu
            $('.treeview > a').on('click', function(e) {
                e.preventDefault();
                var parent = $(this).parent();
                var submenu = parent.find('.treeview-menu');

                // Toggle the submenu
                submenu.slideToggle();
                parent.toggleClass('menu-open');
            });

            // Ensure the "Dashboard" link is clickable
            $('.sidebar-menu a[href="/"]').off('click').on('click', function(e) {
                // Allow the default behavior (navigation to the dashboard)
                // No preventDefault() or stopPropagation() here, so it navigates correctly
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
});
