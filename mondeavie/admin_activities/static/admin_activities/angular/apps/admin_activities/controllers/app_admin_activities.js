
/* global angular */
var appActivitiesAdmin = angular.module('appActivitiesAdmin', ['ngRoute', 'ngCookies', 'ui.bootstrap']);

/* Config */
appActivitiesAdmin.config(function($interpolateProvider) {
    //allow django templates and angular to co-exist
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

appActivitiesAdmin.run(function($rootScope, $log, $http, $cookies, $templateCache) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});


appActivitiesAdmin.directive('ngConfirmClick', [
    function(){
        return {
            link: function (scope, element, attr) {
                var msg = attr.ngConfirmClick || "Are you sure?";
                var clickAction = attr.confirmedClick;
                element.bind('click',function (event) {
                    if ( window.confirm(msg) ) {
                        scope.$eval(clickAction)
                    }
                });
            }
        };
    }
]);

appActivitiesAdmin.directive("ngFileSelectCourse",function(){
    return {
        link: function($scope, el){
            console.log('ngFileSelect=bibi');
            el.bind("change", function(e){          
                $scope.file = (e.srcElement || e.target).files[0];
                $scope.getFileCourse();
            });
        }
    };
});

appActivitiesAdmin.directive("ngFileSelectConference",function(){
    return {
        link: function($scope, el){
            console.log('ngFileSelect=conf');
            el.bind("change", function(e){          
                $scope.file = (e.srcElement || e.target).files[0];
                $scope.getFileConference();
            });
        }
    };
});

appActivitiesAdmin.directive("errormsg",function(){
    return {
        scope:{
            saveError:"@"
        },
        template: '<div style="color:red">{[{ saveError }]}</div>',
        link: function($scope, element, attrs){
            if(attrs.saveError){
                alert('error');
            }
        }
    };
});


// http://stackoverflow.com/questions/22113456/modal-confirmation-as-an-angular-ui-directive
appActivitiesAdmin.directive('ngReallyClick', ['$modal',
    function($modal) {

        var ModalInstanceCtrl = function($scope, $modalInstance) {
            $scope.ok = function() {
                $modalInstance.close();
            };

            $scope.cancel = function() {
                $modalInstance.dismiss('cancel');
            };
        };

        return {
            restrict: 'A',
            scope:{
                ngReallyClick:"&",
                item:"="
            },
            link: function(scope, element, attrs) {
                element.bind('click', function() {
                    var message = attrs.ngReallyMessage || "Are you sure ?";

                    var modalHtml = '<div class="modal-body">' + message + '</div>';
                    modalHtml += '<div class="modal-footer"><button class="btn btn-danger" ng-click="ok()">OUI</button><button class="btn btn-success" ng-click="cancel()">NON</button></div>';

                    //if(scope.item != null && scope.item.id ){
            
                    var modalInstance = $modal.open({
                        template: modalHtml,
                        controller: ModalInstanceCtrl
                    });

                    modalInstance.result.then(function() {
                        scope.ngReallyClick({item:scope.item}); //raise an error : $digest already in progress
                    }, function() {
                        //Modal dismissed
                    });
                });
            }
        }
    }
]);


appActivitiesAdmin.directive('ckEditor', function() {
    return {
        require: '?ngModel',
        link: function(scope, elm, attr, ngModel) {
            var ck = CKEDITOR.replace(elm[0]);

            if (!ngModel) return;

            ck.on('pasteState', function() {
                scope.$apply(function() {
                    ngModel.$setViewValue(ck.getData());
                });
            });

            // http://stackoverflow.com/questions/15483579/angularjs-ckeditor-directive-sometimes-fails-to-load-data-from-a-service
            // Suppose to eleminate the bug of sometime empty window
            ck.on('instanceReady', function() {
                ck.setData(ngModel.$viewValue);
            });

            ngModel.$render = function(value) {
                ck.setData(ngModel.$viewValue);
            };
        }
    };
});


appActivitiesAdmin.service('dataService', function($http) {
    this.get = function(url, callbackFunc) {
        $http({
            method: 'GET',
            url: url
         }).success(function(data){
            // With the data succesfully returned, call our callback
            callbackFunc(data);
        }).error(function(){
            alert("error");
        });
    };

    this.create = function(url, data, callbackFunc) {
        $http({
            method: 'POST',
            data: data,
            url: url
         }).success(function(data){
            // With the data succesfully returned, call our callback
            callbackFunc(data);
        }).error(function(){
            alert("error");
        });
    };

});



appActivitiesAdmin.config(function($routeProvider) {
    // '/static/admin_activities/angular/apps/admin_activities/partials/courses_schedule.html'
    $routeProvider.when('/courses/', {
        templateUrl: '/admin_activities/courses/', 
            controller: function ($scope, $location) {
              $location.path('/admin_activities/courses/');
        },
        controller: 'CalendarCtrl'

    }).when('/conferences/', {
        templateUrl: '/admin_activities/conferences/', 
            controller: function ($scope, $location) {
              $location.path('/admin_activities/conferences/');
        },
        controller: 'CalendarCtrl'

    }).otherwise({
        redirectTo: '/courses/'
    });
});

/*************************************************************************
 * The controller
 ************************************************************************/


appActivitiesAdmin.run(function($templateCache) {
    //$templateCache.put('/dialogs/notify.html','<div class="modal"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><h4 class="modal-title"><span class="glyphicon glyphicon-star"></span> User\'s Name</h4></div><div class="modal-body"><ng-form name="nameDialog" novalidate role="form"><div class="form-group input-group-lg" ng-class="{true: \'has-error\'}[nameDialog.username.$dirty && nameDialog.username.$invalid]"><label class="control-label" for="username">Name:</label><input type="text" class="form-control" name="username" id="username" ng-model="user.name" ng-keyup="hitEnter($event)" required><span class="help-block">Enter your full name, first &amp; last.</span></div></ng-form></div><div class="modal-footer"><button type="button" class="btn btn-default" ng-click="cancel()">Cancel</button><button type="button" class="btn btn-primary" ng-click="save()" ng-disabled="(nameDialog.$dirty && nameDialog.$invalid) || nameDialog.$pristine">Save</button></div></div></div></div>');
});

    
appActivitiesAdmin.factory("fileReader", ["$q", "$log", function($q, $log) {

    var onLoad = function(reader, deferred, scope) {
        return function () {
            scope.$apply(function () {
                deferred.resolve(reader.result);
            });
        };
    };

    var onError = function (reader, deferred, scope) {
        return function () {
            scope.$apply(function () {
                deferred.reject(reader.result);
            });
        };
    };

    var onProgress = function(reader, scope) {
        return function (event) {
            scope.$broadcast("fileProgress",
                {
                    total: event.total,
                    loaded: event.loaded
                });
        };
    };

    var getReader = function(deferred, scope) {
        var reader = new FileReader();
        reader.onload = onLoad(reader, deferred, scope);
        reader.onerror = onError(reader, deferred, scope);
        reader.onprogress = onProgress(reader, scope);
        return reader;
    };

    var readAsDataURL = function (file, scope) {
        var deferred = $q.defer();
         
        var reader = getReader(deferred, scope);         
        reader.readAsDataURL(file);
         
        return deferred.promise;
    };

    return {
            readAsDataUrl: readAsDataURL  
    };
}]);


appActivitiesAdmin.controller('CalendarCtrl', function (
    $scope,
    $routeParams,
    $timeout,
    $rootScope,
    dataService,
    ModelUtils,
    fileReader
    ) {

    $scope.reallyDelete = function(item) {
        $scope.items = window._.remove($scope.items, function(elem) {
          return elem != item;
        });
    };


    $scope.getFileCourse = function() {
        if(!$scope.course){
            $scope.course = {};
        }
        
        fileReader.readAsDataUrl($scope.file, $scope)
                      .then(function(result) {
                          $scope.course.image = {};
                          $scope.course.image.base64 = result;
                          $scope.course.image.name = $scope.file.name;
                      });
    };


    $scope.getFileConference = function() {
        if(!$scope.conference){
            $scope.conference = {};
        }
        
        fileReader.readAsDataUrl($scope.file, $scope)
                      .then(function(result) {
                          $scope.conference.image = {};
                          $scope.conference.image.base64 = result;
                          $scope.conference.image.name = $scope.file.name;
                      });
    };

    var delay = 1;
    var delaySuccessClass = function(objSaved){
        objSaved.success=true;
        $timeout(function(){
            if(delay < 2){
                delay += 1;
                delaySuccessClass(objSaved);
            }else{
                $scope.$apply(function() {
                    objSaved.success=false;
                });                    
            }
        },500);// 500ms
    }; // end delaySuccessClass 

    
    //dlg = $dialogs.create('/dialogs/whatsyourname.html','whatsYourNameCtrl',{},{key: false,back: 'static'});
    var isEmpty = function (obj) {
        for(var prop in obj) {
            if(obj.hasOwnProperty(prop))
                return false;
        }
        return true;
    }

    var objExist = function(obj, objs){
        for (var i = 0; i < objs.length; i++){
            if(obj.id == objs[i].id) {
                return true;
            }
        }
        return false;
    };

    var saveObj = function(obj, objs, url){
        obj.errors = {};
        return ModelUtils.save(url, obj, obj.errors).then(function(response){
            // Push object into objects only if is not exist.
            console.log("objs");
            console.log(objs);
            if(objs) {
                if(objs.indexOf(obj) == -1){
                    objs.push(obj);
                }
            }
            //dlg = $dialogs.wait(msgs[i++],progress);
            //fakeProgress();

        });
    };

    var delObj = function(obj, objs, url){
        ModelUtils.del(url, obj).then(function(response){
            var index =  objs.indexOf(obj);
            if (index > -1) {
                objs.splice(index, 1);
            }
        });
    };


    /* 
        dayNames
    */
    var URL_DAY_NAMES = '/admin_activities/api/day_names/';
    var getDayNames = function(){
        ModelUtils.get(URL_DAY_NAMES, null).then(function(response){
            $scope.dayNames = response.data;
        });
    };

    /* 
        Teacher
    */
    var URL_TEACHERS = '/admin_activities/api/teachers/';
    $scope.newTeacher = function(){
        clearTeacher();
        $scope.isModTeacher = true;
    };

    $scope.modTeacher = function(){
        $scope.isModTeacher = !$scope.isModTeacher;
    };

    $scope.saveTeacher = function(){
        var isSaved = saveObj($scope.teacher, $scope.teachers, URL_TEACHERS);
        isSaved.then(function (res){
            delaySuccessClass($scope.teacher);
            $scope.isModTeacher = false;
        });
    };

    $scope.delCancelTeacher = function(){
        // The function is also called when the obj is not saved
        // so call the rest only if the object has an id.
        console.log('delCancelTeacher');
        if( $scope.teacher != null && $scope.teacher.id != null) {
            delObj($scope.teacher, $scope.teachers, URL_TEACHERS);
        }
        clearTeacher();
        $scope.isModTeacher = false;
    };

    $scope.selectTeacher = function(teacherOpt){
        $scope.teacher = teacherOpt;
    };

    var clearTeacher = function(){
        $scope.teacher = null;
    };

    var getTeachers = function (){
        ModelUtils.get(URL_TEACHERS, null).then(function(response){
            $scope.teachers = response.data;
        });
    };

    $scope.$watch('teacher', function(newValue, oldValue) {
        getCourse();
    });

    /*
    $scope.$watch('teachers.length', function(newValue, oldValue) {
        //getTeachers()
    });
    */

    /* 
        CourseName
    */
    var URL_COURSE_NAMES = '/admin_activities/api/course_names/';
    $scope.newCourseName = function(){
        $scope.courseName = null;
        $scope.isModCourseName = true;
    };

    $scope.modCourseName = function(){
        $scope.isModCourseName = !$scope.isModCourseName;
    };

    $scope.saveCourseName = function(){
        var isSaved = saveObj($scope.courseName, $scope.courseNames, URL_COURSE_NAMES);
        isSaved.then(function (res){
            delaySuccessClass($scope.courseName);
            $scope.isModCourseName = false;
        });
    };

    $scope.delCancelCourseName = function(){
        if( $scope.courseName != null && $scope.courseName.id != null) {
            delObj($scope.courseName, $scope.courseNames, URL_COURSE_NAMES);
        }
        clearCourseName();
        $scope.isModCourseName = false;
    };

    $scope.selectCourseName = function(courseNameOpt){
        $scope.courseName = courseNameOpt;
    };

    var clearCourseName = function(){
        $scope.courseName = null;
    };

    var getCourseNames = function (){
        clearCourseName();
        ModelUtils.get(URL_COURSE_NAMES, null).then(function(response){
            $scope.courseNames = response.data;
        });
    };

    $scope.$watch('courseName', function(newValue, oldValue) {
        getCourse();
    });

    /*
        Course
    */
    var URL_COURSES = '/admin_activities/api/courses/';
    $scope.newCourse = function(){
        $scope.course = {};
        $scope.course.is_visible = true;
        $scope.isModCourse = true;
    };

    $scope.modCourse = function(){
        $scope.isModCourse = !$scope.isModCourse;
    };

    $scope.saveCourse = function(){
        $scope.course.teacher = $scope.teacher.id;
        $scope.course.course_name = $scope.courseName.id;

        var isSaved = saveObj($scope.course, [], URL_COURSES);
        isSaved.then(function (res){
            delaySuccessClass($scope.course);
            $scope.isModCourse = false;
        });
    };

    $scope.delCancelCourse = function(){
        if( $scope.course != null && $scope.course.id != null) {
            delObj($scope.course, [], URL_COURSES);
        }
        clearCourse();
        $scope.isModCourse = false;
    };

    var clearCourse = function(){
        $scope.course = null;
        $scope.isModCourse = false;
    };


    var getCourse = function (){
        clearCourse();
        if( $scope.teacher != null && $scope.teacher.id &&
            $scope.courseName != null && $scope.courseName.id){
            var url = URL_COURSES + '?teacher=' + $scope.teacher.id + 
                        '&course_name=' + $scope.courseName.id;
            ModelUtils.get(url, null).then(function(response){
                $scope.course = response.data[0];
            });
        }
    };

    $scope.$watch('course', function(newValue, oldValue) {
        getSchedules();
    });

    /* 
        schedule
    */
    var URL_SCHEDULE = '/admin_activities/api/schedules/';
    $scope.newSchedule = function(){
        $scope.schedule = {};
        $scope.isModSchedule = true;
    };

    $scope.modSchedule = function(){
        $scope.isModSchedule = !$scope.isModSchedule;
    };

    $scope.saveSchedule = function(){
        // Need to assign the current corse id to the selected schedule
        $scope.schedule.course = $scope.course.id;

        var isSaved = saveObj($scope.schedule, $scope.schedules, URL_SCHEDULE);
        isSaved.then(function (res){
            delaySuccessClass($scope.schedule);
            $scope.isModSchedule = false;
        });
    };

    $scope.delCancelSchedule = function(){
        if( $scope.schedule != null && $scope.schedule.id != null) {
            delObj($scope.schedule, $scope.schedules, URL_SCHEDULE);
        }
        $scope.schedule = null;
        $scope.isModSchedule = false;
    };

    $scope.selectSchedule = function(scheduleOpt){
        $scope.schedule = scheduleOpt;
    };

    var clearSchedule = function(){
        $scope.schedule = null;
        $scope.schedules = null;
    };


    var getSchedules = function (){
        clearSchedule();
        if($scope.course != null && $scope.course.id ){
            var url = URL_SCHEDULE + '?course=' + $scope.course.id;
            ModelUtils.get(url, null).then(function(response){
                $scope.schedules = response.data;
            });
        }
    };

    $scope.$watch('schedule', function(newValue, oldValue) {
        console.log('watch schedule.id');
        getDaySchedules();
    });




        

    /* 
        daySchedule 
    */
    var URL_DAY_SCHEDULES = '/admin_activities/api/day_schedules/';

    var getDayNameName = function(day_name_id){
        if($scope.dayNames != null) {
            for (var i = 0; i < $scope.dayNames.length; i++){
                if(day_name_id == $scope.dayNames[i].id) {
                    return $scope.dayNames[i].name;
                }
            }
        }
        return "";
    };

    $scope.saveDaySchedule = function(){

        $scope.daySchedule.schedule = $scope.schedule.id;
        
        var isSaved = saveObj($scope.daySchedule, $scope.daySchedules, URL_DAY_SCHEDULES);
        isSaved.then(function (res){
            $scope.isModDaySchedule = !$scope.isModDaySchedule;
            delaySuccessClass($scope.daySchedule);
        });
    };

    $scope.saveDayScheduleNew = function(){
        $scope.dayScheduleNew.schedule = $scope.schedule.id;
        if(!$scope.daySchedules){
            $scope.daySchedules = [];
        }

        var isSaved = saveObj($scope.dayScheduleNew, $scope.daySchedules, URL_DAY_SCHEDULES);
        isSaved.then(function (res){
            delaySuccessClass($scope.dayScheduleNew);
            $scope.dayScheduleNew = {};
        });

        
    };

    $scope.delCancelDaySchedule = function(daySchedule){
        console.log('delCancelSchedule');
        if(daySchedule != null && daySchedule.id ){
            delObj(daySchedule, $scope.daySchedules, URL_DAY_SCHEDULES);
            getDaySchedules();
        }else{
            daySchedule.hour_start = "";
            daySchedule.hour_end = "";
            daySchedule.day_name = null;
            daySchedule.day_name_name = null;
        }
        // colapse
        $scope.isModDaySchedule = false;
    };



    $scope.selectDayName = function(dayName, daySchedule){
        console.log(daySchedule);
        daySchedule.day_name = dayName.id;
        daySchedule.day_name_name = getDayNameName(dayName.id);
    };



    var clearDaySchedule = function(){
        $scope.daySchedule = null;
        $scope.daySchedules = null;
        $scope.isModDaySchedule = false;
    };

    var getDaySchedules = function (){
        clearDaySchedule();
        if($scope.schedule != null && $scope.schedule.id){
            var url = URL_DAY_SCHEDULES + '?schedule=' + $scope.schedule.id;
            ModelUtils.get(url, null).then(function(response){
                $scope.daySchedules = response.data;
                console.log(response.data);
                for (var i = 0; i < $scope.daySchedules.length; i++){
                    $scope.daySchedules[i].day_name_name = 
                            getDayNameName($scope.daySchedules[i].day_name);
                }
            });
        }
    };


    $scope.selectDaySchedule = function(dayScheduleOpt){
        $scope.daySchedule = dayScheduleOpt;
    };


    $scope.modDaySchedule = function(){
        $scope.isModDaySchedule = !$scope.isModDaySchedule;
    };

    $scope.newDaySchedule = function(){
        $scope.daySchedule = {};
        $scope.isModDaySchedule = true;
    };


    $scope.$watch('daySchedule', function(newValue, oldValue) {
        console.log('watch daySchedule.id');
        getTestingDays();
    });

    /* 
        daySchedule 
    */
    var URL_TESTING_DAYS = '/admin_activities/api/testing_days/';


    var clearTestingDay = function(){
        $scope.testingDay = null;
        $scope.testingDays = null;
        $scope.isModTestingDay = false;
    };

    var getTestingDays = function (){
        clearTestingDay();
        if($scope.daySchedule != null && $scope.daySchedule.id){
            var url = URL_TESTING_DAYS + '?day_schedule=' + $scope.daySchedule.id;
            ModelUtils.get(url, null).then(function(response){
                $scope.testingDays = response.data;
                console.log(response.data);
            });
        }
    };

    var tmp = function(){
        $scope.daySchedule = {};
        $scope.daySchedule.id=1;
    };

    //tmp();
    //getTestingDays();
    $scope.saveTestingDay = function(){
        $scope.testingDay.day_schedule = $scope.daySchedule.id;
        
        var isSaved = saveObj($scope.testingDay, $scope.testingDays, URL_TESTING_DAYS);
        isSaved.then(function (res){
            $scope.isModTestingDay = !$scope.isModTestingDay;
            delaySuccessClass($scope.testingDay);
        });
    };


    $scope.delCancelTestingDay = function(testingDay){
        console.log('delCancelSchedule');
        if(testingDay != null && testingDay.id ){
            delObj(testingDay, $scope.testingDays, URL_TESTING_DAYS);
            getTestingDays();
        }else{
            testingDay.hour_start = "";
            testingDay.hour_end = "";
            testingDay.day_name = null;
            testingDay.day_name_name = null;
        }
        // colapse
        $scope.isModTestingDay = false;
    };



    $scope.selectDayName = function(dayName, testingDay){
        console.log(testingDay);
        testingDay.day_name = dayName.id;
        testingDay.day_name_name = getDayNameName(dayName.id);
    };









    $scope.selectTestingDay = function(testingDayOpt){
        $scope.testingDay = testingDayOpt;
    };


    $scope.modTestingDay = function(){
        $scope.isModTestingDay = !$scope.isModTestingDay;
    };

    $scope.newTestingDay = function(){
        $scope.testingDay = {};
        $scope.isModTestingDay = true;
    };


    $scope.dayScheduleNew = {};
    $scope.daySchedules = {};

    getCourseNames();
    getTeachers();
    getDayNames();

    /*
    Conference and activities
    */



    /* 
        Speaker
    */
    var URL_SPEAKERS = '/admin_activities/api/speakers/';
    $scope.newSpeaker = function(){
        clearSpeaker();
        $scope.isModSpeaker = true;
    };

    $scope.modSpeaker = function(){
        $scope.isModSpeaker = !$scope.isModSpeaker;
    };

    $scope.saveSpeaker = function(){
        var isSaved = saveObj($scope.speaker, $scope.speakers, URL_SPEAKERS);
        isSaved.then(function (res){
            delaySuccessClass($scope.speaker);
            $scope.isModSpeaker = false;
        });
    };

    $scope.delCancelSpeaker = function(){
        // The function is also called when the obj is not saved
        // so call the rest only if the object has an id.
        if( $scope.speaker != null && $scope.speaker.id != null) {
            delObj($scope.speaker, $scope.speakers, URL_SPEAKERS);
        }
        clearSpeaker();
        $scope.isModSpeaker = false;
    };

    $scope.selectSpeaker = function(speakerOpt){
        $scope.speaker = speakerOpt;
    };

    var clearSpeaker = function(){
        $scope.speaker = null;
    };

    var getSpeakers = function (){
        ModelUtils.get(URL_SPEAKERS, null).then(function(response){
            $scope.speakers = response.data;
        });
    };

    $scope.$watch('speaker', function(newValue, oldValue) {
        console.log('getEvent()');
        $scope.hideAdd = false;
    });

    /* 
        Conference
    */
    var URL_CONFERENCES = '/admin_activities/api/conferences/';
    var URL_CONFERENCES_NESTED = '/admin_activities/api/nested/speakers/conferences/';
    $scope.newConference = function(){
        clearConference();
        $scope.conference = {};
        $scope.conference.is_visible = true;
        $scope.conference.speakers = [];
        $scope.isModConference = true;
    };

    $scope.modConference = function(){
        $scope.isModConference = !$scope.isModConference;
    };

    $scope.saveConference = function(){
        var speakersCopy = $scope.conference.speakers;
        var idArray = [];
        for (var i = 0; i < $scope.conference.speakers.length; i++){
            idArray.push(parseInt($scope.conference.speakers[i].id));
        }

        $scope.conference.speakers = idArray;
        var isSaved = saveObj($scope.conference, $scope.conferences, URL_CONFERENCES);
        isSaved.then(function (res){
            $scope.conference.speakers = speakersCopy;
            delaySuccessClass($scope.conference);
            $scope.isModConference = false;
        });
    };


    $scope.delSpeakerFromConf = function(speaker){
        var objs = $scope.conference.speakers;
        var obj = speaker;
        var index =  objs.indexOf(obj);
        if (index > -1) {
            objs.splice(index, 1);
        }
    };


    $scope.addSpeakerFromConf = function(){
        var obj = $scope.speaker;
        var objs = $scope.conference.speakers;

        // if object do not exist in the list
        if(objs && !objExist(obj, objs)) {
            objs.push(obj);
        }
        $scope.hideAdd = true;
    };

    

    $scope.delCancelConference = function(){
        // The function is also called when the obj is not saved
        // so call the rest only if the object has an id.
        if( $scope.conference != null && $scope.conference.id != null) {
            delObj($scope.conference, $scope.conferences, URL_CONFERENCES);
        }
        clearConference();
        $scope.isModConference = false;
    };

    $scope.selectConference = function(conferenceOpt){
        $scope.conference = conferenceOpt;
    };

    var clearConference = function(){
        $scope.conference = null;
    };

    var getConferences = function (){
        ModelUtils.get(URL_CONFERENCES_NESTED, null).then(function(response){
            $scope.conferences = response.data;
        });
    };

    var isSpeakerExist = function(){
        if ($scope.conference && $scope.speaker){
            var obj = $scope.speaker;
            var objs = $scope.conference.speakers;
            $scope.conference.disableAddSpeaker = objExist(obj, objs);
        }else {
            if($scope.conference) {
                $scope.conference.disableAddSpeaker = true;
            }
        }
    };
    $scope.$watch('conference', function(newValue, oldValue) {
        console.log('conference change');
        getDayConferences();
    });

    /* 
        dayConference 
    */
    var URL_DAY_CONFERENCE = '/admin_activities/api/day_conferences/';


    $scope.selectDayConference = function(dayConferenceOpt){
        $scope.dayConference = dayConferenceOpt;
    };


    $scope.modDayConference = function(){
        $scope.isModDayConference = !$scope.isModDayConference;
    };

    $scope.newDayConference = function(){
        $scope.dayConference = {};
        $scope.isModDayConference = true;
    };

    $scope.saveDayConference = function(dayConference){
        dayConference.conference = $scope.conference.id;
        
        var isSaved = saveObj(dayConference, $scope.dayConferences, URL_DAY_CONFERENCE);
        isSaved.then(function (res){
            delaySuccessClass(dayConference);
            $scope.isModDayConference = false;
        });
    };


    $scope.delCancelDayConference = function(dayConference){
        console.log('delCancelSchedule');
        if(dayConference != null && dayConference.id ){
            delObj(dayConference, $scope.dayConferences, URL_DAY_CONFERENCE);
            getDayConferences();
        }else{
            dayConference.hour_start = "";
            dayConference.hour_end = "";
            dayConference.day = null;
        }

        // colapse
        $scope.isModDayConference = false;
    };


    var clearDayConference = function(){
        $scope.dayConference = null;
        $scope.dayConferences = null;
    };

    var getDayConferences = function (){
        clearDayConference();
        if($scope.conference != null && $scope.conference.id){
            var url = URL_DAY_CONFERENCE + '?conference=' + $scope.conference.id;
            ModelUtils.get(url, null).then(function(response){
                $scope.dayConferences = response.data;
            });
        }
    };

    /*
    $scope.$watch('dayConferences.length', function(newValue, oldValue) {
        getDayConferences();
    });
    */

    $scope.dayConferenceNew = {};
    $scope.dayConferences = {};

    getSpeakers();
    getConferences();
}); // end run / module

