# Django app for Performance Monitoring with Google Analytics

Send perfomance data to Google Analytics, you can view it in Content > Site Speed > User Timings.
Heavily inspired by <a href="https://github.com/jsuchal/garelic">Garelic Rails gem</a> by Jan Suchal.

## Installation.

1. **Download**
    
    pip install git+https://github.com/junckritter/gadjango

2. **Add middleware to your settings**
    
    MIDDLEWARE_CLASSES = (
       'gadjango.middleware.TimingMiddleware',
        ...
        ...
    )    
    
3. **Include HTML template in Google Analytics JavaScript element 
    
    <script type="text/javascript">
        var _gaq = _gaq || [];
        _gaq.push(['_setAccount', 'UA-XXXXXXXX-X']);
        _gaq.push(['_setSiteSpeedSampleRate', 100]);
        _gaq.push(['_trackPageview']);

        {% include "gadjango/timing.html" %}

        (function() {
            var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
            ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
        })();
    </script>

