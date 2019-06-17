$(document).ready(function() {
    $('.expandable-header').click(function(e) {
        e.preventDefault();

        var $header = $(this);
        var $content = $header.nextAll('.expandable-content');

        if ($content.is(':visible')) {
            $content.slideUp('fast');
        } else {
            $content.slideDown('fast');
        }
    });

    SyntaxHighlighter.all();

    $(".tabsContainer").tabs();

    $('.contains-issues')
        .find('[data-issue]')
        .each(function() {

            var $this = $(this);
            var issueIds = $this.attr('data-issue');
            if (!issueIds) {
                return;
            }

            $this.append(' [');

            var issueList = issueIds.split(',');
            $.each(issueList, function(index, issueId) {
                if (index > 0) {
                    $this.append(', ');
                }

                $('<a />')
                    .text('#' + issueId)
                    .attr('href', 'https://github.com/hikalkan/jtable/issues/' + issueId)
                    .attr('target', '_blank')
                    .appendTo($this);
            });

            $this.append(']');

        });
});