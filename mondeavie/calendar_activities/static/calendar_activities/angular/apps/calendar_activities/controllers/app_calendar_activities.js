


/*************************************************************************
 * App
 ************************************************************************/
var appCalendar = angular.module('appCalendar', ['ngRoute', 'ngCookies',
    'ngAnimate']);


/*************************************************************************
 * Configuration
 ************************************************************************/
appCalendar.config(function($interpolateProvider, $routeProvider) {
    //allow django templates and angular to co-exist
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');

    /* Courses */
    $routeProvider.when('/courses/', {
        templateUrl: '/calendar_activities/calendar_builder/',
        controller: 'CourseCtrl'

    }).when('/courses/:courseID', {
        templateUrl: '/calendar_activities/partials/course_detail.html',
        controller: 'CourseDetailCtrl'

    }).when('/day_schedules/reserve/:dayScheduleID', {
        templateUrl: '/calendar_activities/partials/reserve_day_schedule.html',
        controller: 'DayScheduleReserveCtrl'

    /* Conferences */
    }).when('/conferences/', {
        templateUrl: '/calendar_activities/conferences/',
        controller: 'ConferenceCtrl'

    }).when('/conferences/:conferenceID', {
        templateUrl: '/calendar_activities/partials/conference_detail.html',
        controller: 'ConferenceDetailCtrl'

    }).when('/day_conferences/reserve/:dayConferenceID', {
        templateUrl: '/calendar_activities/partials/reserve_day_conference.html',
        controller: 'DayConferenceReserveCtrl'

    /* By default, redirect to #/courses/ */
    }).otherwise({
        redirectTo: '/courses/'
    });
});

/*************************************************************************
 * run, startup
 ************************************************************************/
/* http header needed by django */
appCalendar.run(function($rootScope, $log, $http, $cookies, $templateCache) {
    // Always set the CSRFToken when it POST
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    // If this variable is not set, request.POST return empty QueryDict<>
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

});


/*************************************************************************
 * The Services
 ************************************************************************/
appCalendar.factory('ModelUtils', function($http, $log) {

    var handleErrors =  function(serverResponse, status, errorDestination) {
        if (angular.isDefined(errorDestination)) {
            if (status >= 500) {
                errorDestination.form = 'Server Error: ' + status;
            } else if (status >= 401) {
                errorDestination.form = 'Unauthorized Error: ' + status;
            } else {
                angular.forEach(serverResponse, function(value, key) {
                    console.log(serverResponse);
                    if (key != '__all__') {
                        errorDestination[key] = angular.isArray(value) ? value.join("<br/>") : value;
                    } else {
                        errorDestination.form = errorDestination.form || '' + key + ':' + angular.isArray(value) ? value.join("<br/>") : value;
                    }
                });
            }
        }
        console.log(errorDestination);
    };

    var ModelUtils = {
        get: function(url, id) {
            if (id != null) {
                return $http.get(url + id);
            }else {
                return $http.get(url);
            }
        },
        create: function(url, obj, errors) {
            console.log('create');
            return $http.post(url, obj).
                success(function(response, status, headers, config) {
                    // Object to object copies
                    //angular.extend(obj, response);
                    handleErrors(response, status, errors);
                }).
                error(function(response, status, headers, config) {
                    handleErrors(response, status, errors);
                });
        },
        save: function(url, obj, errors) {
            if (obj.id != null) {
                return $http.put(url + obj.id, obj).
                        success(function(response, status, headers, config) {
                            angular.extend(obj, response);
                        }).
                        error(function(response, status, headers, config) {
                            handleErrors(response, status, errors);
                        });
            } else {
                return this.create(url, obj, errors);
            }
        },
        del: function(url, obj) {
            return $http.delete(url + obj.id);
        }
    };
    return ModelUtils;
});

/* Go to TOP top-anchor, used when each controllers is loaded */
appCalendar.factory('GoTopFactory', function ($location, $anchorScroll) {
    return function(){
        $location.hash('top-anchor');
        $anchorScroll();
    };
});

/*
Convert :
    (2014-01-01, 2014-01-03) -> "1 Janvier au 3 Janvier 2014"
    (2014-01-01, 2015-01-03) -> "1 Janvier 2014 au 3 Janvier 2015"
*/
appCalendar.factory('DateRange', function() {

    var getYear = function(date){
        var date_array = date.split("-");
        return date_array[0];
    };

    var getMonthStr = function(monthNumber){
        switch(monthNumber) {
            case 1:
                return "Janvier";
                break;
            case 2:
                return "Février";
                break;
            case 3:
                return "Mars";
                break;
            case 4:
                return "Avril";
                break;
            case 5:
                return "Mai";
                break;
            case 6:
                return "Juin";
                break;
            case 7:
                return "Juillet";
                break;
            case 8:
                return "Août";
                break;
            case 9:
                return "Septembre";
                break;
            case 10:
                return "Octobre";
                break;
            case 11:
                return "Novembre";
                break;
            case 12:
                return "Décembre";
                break;  
        }
    };

    var getMonth = function(date){
        var date_array = date.split("-");
        return getMonthStr(parseInt(date_array[1]));
    };

    var getDay = function(date){
        var date_array = date.split("-");
        return date_array[2];
    };

    var DateRange = {
        getDateRange : function(day_start, day_end){
            var day_start_str = getDay(day_start) + " " +
                getMonth(day_start);

            if(getYear(day_start) != getYear(day_end)){
                day_start_str += " " + getYear(day_start)
            }
            var day_end_str = getDay(day_end) + " " +
                getMonth(day_end) + " " + getYear(day_end);

            return day_start_str + " au " + day_end_str;
        }
    };
    return DateRange;
});

/*************************************************************************
 * Course controller
 ************************************************************************/
appCalendar.controller('CourseCtrl', function (
    $scope,
    $routeParams,
    $timeout,
    $rootScope,
    ModelUtils
    ) {


    /* 
        courseName with nested course.id and course.teacher.name
    */
    var URL_COURSE_NAME_NESTED_COURSES =
        '/calendar_activities/api/nested/courses/course_name/';
    var getAllCourseNameNestedCourses = function (id){
        ModelUtils.get(URL_COURSE_NAME_NESTED_COURSES, id).then(function(response){
            $scope.courseNameCourses = response.data;
        });
    };

    getAllCourseNameNestedCourses();

    $scope.UrlCourseDetail =
        '/calendar_activities/api/nested/courses/course_name/';
});

/*************************************************************************
 * Course Detail controller
 ************************************************************************/
appCalendar.controller('CourseDetailCtrl', function (
    $scope,
    $routeParams,
    $timeout,
    $rootScope,
    $sce,
    ModelUtils,
    DateRange
    ){

    $scope.getTrustAsHtml = function(value){
        return $sce.trustAsHtml(value);
    };

    $scope.getRangeDateStr = function(day_start, day_end){
        return DateRange.getDateRange(day_start, day_end);
    };

    /* 
        courseDetail 
    */
    var URL_COURSE_NESTED_CHILDS =
        '/calendar_activities/api/nested/childs/courses/';

    var getCourseNestedChilds = function (id){
        ModelUtils.get(URL_COURSE_NESTED_CHILDS, id).then(function(response){
            $scope.courseDetail = response.data;
        });
    };
    getCourseNestedChilds($routeParams.courseID);
});

/*************************************************************************
 * Day Schedule Reserve controller
 ************************************************************************/
appCalendar.controller('DayScheduleReserveCtrl', function (
    $scope,
    $routeParams,
    $rootScope,
    $sce,
    $window,
    ModelUtils
    ) {


    $scope.reservation = {};
    $scope.reservation.client = {}
    $scope.reservation.client.selections = [];
    console.log($scope.reservation.client.selections);
    // toggle selection for a given fruit by name
    $scope.toggleSelection = function toggleSelection(day) {

        var idx = $scope.reservation.client.selections.indexOf(day);

        // is currently selected
        if (idx > -1) {
            $scope.reservation.client.selections.splice(idx, 1);
        }

        // is newly selected
        else {
            $scope.reservation.client.selections.push(day);
        }
    };

    var resetViews = function(){
        $scope.isTestingDay = false;
        $scope.isDayInterval = false;
        $scope.isDay = false;
        $scope.isTryingDay = false;
        $scope.isForm = false;
        $scope.reservation.client.selections = [];
        $scope.reservation.client.isSelections = false;
        $scope.reservation.client.errors = {};
        $scope.currentTableDays = {};
    };


    $scope.selectItem = function(item){
        $scope.item = item;
        resetViews();
        item.funct();
        $scope.reservation.client.currentMenu = item.label;
    };


    var selectTestingDay = function(){
        console.log('selectTestingDay');
        $scope.isTestingDay = true;
        $scope.isForm = true;
        $scope.reservation.client.isSelections = true;
        $scope.currentTableDays = $scope.reservation.testingDays.list;
    };

    var selectDayInterval = function(){
        console.log('selectDayInterval');
        $scope.isDayInterval = true;
        $scope.isForm = true;
    };

    var selectDay = function(){
        console.log('selectDay');
        $scope.isDay = true;
        $scope.isForm = true;
        $scope.reservation.client.isSelections = true;
        $scope.currentTableDays = $scope.reservation.dayRange.list;
    };

    var selectTryingDay = function(){
        console.log('selectTryingDay');
        $scope.isTryingDay = true;
        $scope.isForm = true;
        $scope.reservation.client.isSelections = true;
        $scope.currentTableDays = $scope.reservation.dayRange.list;
    };

    var setSelect = function(){
        $scope.reservation.client.currentMenu = "Choisir une option de r&eacute;servation";
        $scope.items = [
            {
                label: $scope.reservation.dayRange.dayInterval,
                funct: function(){
                    return selectDayInterval();
                }
            },
            {
                label: "Une ou plusieurs journ&eacute;e(s) de cours",
                funct: function(){
                    return selectDay();
                }
            },
            {
                label: "Un cours d'essai",
                funct: function(){
                    return selectTryingDay();
                }
            },
        ];

        // If is a free course add the choice at the beginning
        if(Object.keys($scope.reservation.testingDays.list).length > 0) {
            $scope.items.unshift(
                {
                    label: "Une Cours Gratuit",
                    funct: function(){
                        return selectTestingDay();
                    }
                }
            );
        }
    };

    $scope.getTrustAsHtml = function(value){
        return $sce.trustAsHtml(value);
    };

    /* 
        scheduleDetail 
    */
    var URL_RESERVE_DAY_SCHEDULES = 
        '/calendar_activities/json/reserve/day_schedules/';

    
    var getReserveDaySchedule = function ( id ){
        
        ModelUtils.get(URL_RESERVE_DAY_SCHEDULES, id).then(function(response){
            $scope.reservation = response.data;
            setSelect();
        });
    };

    getReserveDaySchedule($routeParams.dayScheduleID);


    $scope.send = function(){
        $scope.send_button_disable = true;
        var id = $routeParams.dayScheduleID;
        var url = URL_RESERVE_DAY_SCHEDULES + id;
        var obj = $scope.reservation.client;
        obj.errors = {};

        ModelUtils.save(url, obj, obj.errors).
        success(function(data, status, headers, config) {
            $scope.send_button_disable = false;
            if(!data.errors) { // If no errors 
                $scope.reservation.success = true;
            } else { //if errors
                obj.errors = data.errors;
            }
        }).
        error(function(data, status, headers, config) { 
        // Never called, to remove
        // called asynchronously if an error occurs
        // or server returns response with an error status.
            $scope.send_button_disable = false;
        });
    };
});

/*************************************************************************
 * Conference controller
 ************************************************************************/
appCalendar.controller('ConferenceCtrl', function (
    $scope,
    $routeParams,
    $timeout,
    $rootScope,
    ModelUtils
    ) {

});

/*************************************************************************
 * Conference Detail controller
 ************************************************************************/
appCalendar.controller('ConferenceDetailCtrl', function (
    $scope,
    $routeParams,
    $timeout,
    $rootScope,
    $sce,
    $window,
    ModelUtils
    ) {


    $scope.getTrustAsHtml = function(value){
        return $sce.trustAsHtml(value);
    };

    /* 
        conferenceDetail 
    */
    var URL_CONFERENCE_NESTED_CHILDS =
        '/calendar_activities/api/nested/childs/conferences/';
    var getConferenceNestedChilds = function (id){
        ModelUtils.get(URL_CONFERENCE_NESTED_CHILDS, id).then(function(response){
            $scope.conferenceDetail = response.data;
        });
    };

    getConferenceNestedChilds($routeParams.conferenceID);
});

/*************************************************************************
 * Day Conference Reserve controller
 ************************************************************************/
appCalendar.controller('DayConferenceReserveCtrl', function (
    $scope,
    $routeParams,
    $rootScope,
    $sce,
    $http,
    ModelUtils
    ) {


    $scope.getTrustAsHtml = function(value){
        return $sce.trustAsHtml(value);
    };

    /* 
        conferenceDetail 
    */
    var URL_RESERVE_DAY_CONFERENCES =
        '/calendar_activities/json/reserve/day_conferences/';


    var getReserveDayConference = function ( id ){
        
        ModelUtils.get(URL_RESERVE_DAY_CONFERENCES, id).then(function(response){
            $scope.reservation = response.data;
            $scope.isForm = true;
            $scope.reservation.client.currentMenu = " ";
        });
    };

    getReserveDayConference($routeParams.dayConferenceID);


    $scope.send = function(){
        $scope.send_button_disable = true;
        var id = $routeParams.dayConferenceID;
        var url = URL_RESERVE_DAY_CONFERENCES + id;
        var obj = $scope.reservation.client;
        obj.errors = {};

        ModelUtils.save(url, obj, obj.errors).
        success(function(data, status, headers, config) {
            $scope.send_button_disable = false;
            if(!data.errors) { // If no errors 
                $scope.reservation.success = true;
            } else { //if errors
                obj.errors = data.errors;
            }
        }).
        error(function(data, status, headers, config) { 
        // Never called, to remove
        // called asynchronously if an error occurs
        // or server returns response with an error status.
            $scope.send_button_disable = false;
        });
    };
});