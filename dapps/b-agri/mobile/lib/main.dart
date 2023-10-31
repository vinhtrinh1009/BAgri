import 'dart:async';
import 'package:connectivity/connectivity.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:fluro/fluro.dart';
import 'package:flutter/material.dart' hide Router;
import 'package:flutter/services.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/blocs/navigation/navigation_cubit.dart';

import 'package:flutter_base/commons/app_themes.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'package:flutter_base/network/api_weather.dart';

import 'package:flutter_base/repositories/auth_repository.dart';
import 'package:flutter_base/repositories/farmer_repository.dart';

import 'package:flutter_base/repositories/garden_repository.dart';
import 'package:flutter_base/repositories/notification_repository.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:flutter_base/repositories/season_repository.dart';
import 'package:flutter_base/repositories/task_repository.dart';
import 'package:flutter_base/repositories/tree_repository.dart';
import 'package:flutter_base/repositories/upload_repository.dart';
import 'package:flutter_base/repositories/user_repository.dart';
import 'package:flutter_base/repositories/weather_repository.dart';

import 'package:flutter_base/router/navigation_observer.dart';
import 'package:flutter_base/ui/pages/notification_management/notification_management_cubit.dart';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:get/get.dart';
import 'package:overlay_support/overlay_support.dart';
import 'generated/l10n.dart';

import 'network/api_client_bagri.dart';
import 'network/api_util.dart';

import 'router/application.dart';
import 'router/routers.dart';

final appNavigatorKey = GlobalKey<NavigatorState>();

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
  //black
  SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle.dark);
}

class MyApp extends StatefulWidget {
  MyApp() {
    final router = new FluroRouter();
    Routes.configureRoutes(router);
    Application.router = router;
  }

  @override
  State<StatefulWidget> createState() {
    return _MyAppState();
  }
}

class _MyAppState extends State<MyApp> {
  // b-agri
  ApiClient? _apiClient;
  ApiWeather? _apiWeather;
  final Connectivity _connectivity = Connectivity();
  late StreamSubscription<ConnectivityResult> _connectivitySubscription;
  OverlaySupportEntry? _overlaySupportEntry;
  bool networkEnabled = true;
  NavigationCubit? _navigationCubit;
  // late DynamicConfigCubit _dynamicConfigCubit;

  @override
  void initState() {
    super.initState();
    _apiClient = ApiUtil.getApiClient();
    _apiWeather = ApiUtil.getApiWeather();
    _navigationCubit = NavigationCubit();
    // _dynamicConfigCubit = DynamicConfigCubit();
    initConnectivity();
    _connectivitySubscription =
        _connectivity.onConnectivityChanged.listen(_updateConnectionStatus);
  }

  // Platform messages are asynchronous, so we initialize in an async method.
  Future<void> initConnectivity() async {
    ConnectivityResult? result;
    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      result = await _connectivity.checkConnectivity();
    } on PlatformException catch (e) {
      print(e.toString());
    }

    // If the widget was removed from the tree while the asynchronous platform
    // message was in flight, we want to discard the reply rather than calling
    // setState to update our non-existent appearance.
    if (!mounted) {
      return Future.value(null);
    }

    return _updateConnectionStatus(result);
  }

  Future<void> _updateConnectionStatus(ConnectivityResult? result) async {
    if (result != ConnectivityResult.wifi &&
        result != ConnectivityResult.mobile) {
      if (networkEnabled) {
        _overlaySupportEntry = showSimpleNotification(
          Container(
            child: Text('Không thể kết nối tới máy chủ.'),
          ),
          // contentPadding: EdgeInsets.all(1),
          leading: Icon(Icons.wifi, color: Colors.white),
          autoDismiss: false,
          slideDismiss: false,
          background: Colors.red,
        );
      }
      networkEnabled = false;
    } else {
      networkEnabled = true;
      _overlaySupportEntry?.dismiss(animate: true);
    }
  }

  @override
  void dispose() {
    _navigationCubit!.close();
    // _dynamicConfigCubit.close();
    _connectivitySubscription.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MultiRepositoryProvider(
      providers: [
        RepositoryProvider<AuthRepository>(create: (context) {
          return AuthRepositoryImpl(_apiClient);
        }),
        RepositoryProvider<GardenRepository>(create: (context) {
          return GardenRepositoryImpl(_apiClient);
        }),
        RepositoryProvider<ProcessRepository>(create: (context) {
          return ProcessRepositoryImpl(_apiClient);
        }),
        RepositoryProvider<TreeRepository>(create: (context) {
          return TreeRepositoryImpl(_apiClient);
        }),
        RepositoryProvider<FarmerRepository>(create: (context) {
          return FarmerRepositoryImpl(_apiClient);
        }),
        RepositoryProvider<NotificationRepository>(create: (context) {
          return NotificationRepositoryImpl(_apiClient);
        }),
        RepositoryProvider<SeasonRepository>(create: (context) {
          return SeasonRepositoryImpl(_apiClient);
        }),
        RepositoryProvider<TaskRepository>(create: (context) {
          return TaskRepositoryImpl(_apiClient);
        }),
        RepositoryProvider<UserRepository>(create: (context) {
          return UserRepositoryImpl(_apiClient);
        }),
        RepositoryProvider<WeatherRepository>(create: (context) {
          return WeatherRepositoryImpl(_apiWeather);
        }),
        RepositoryProvider<UploadRepository>(create: (context) {
          return UploadRepositoryImpl(_apiClient);
        }),
        // RepositoryProvider<GlobalDataRepository>(create: (context) {
        //   return GlobalDataRepositoryImpl(_apiClient);
        // }),
      ],
      child: MultiBlocProvider(
        providers: [
          BlocProvider<AppCubit>(create: (context) {
            final _treeRepository =
                RepositoryProvider.of<TreeRepository>(context);
            final _processRepository =
                RepositoryProvider.of<ProcessRepository>(context);
            final _gardenRepository =
                RepositoryProvider.of<GardenRepository>(context);
            final _authRepository =
                RepositoryProvider.of<AuthRepository>(context);
            final _taskRepository =
                RepositoryProvider.of<TaskRepository>(context);
            final _userRepository =
                RepositoryProvider.of<UserRepository>(context);
            final _farmerRepository =
                RepositoryProvider.of<FarmerRepository>(context);
            final _weatherRepository =
                RepositoryProvider.of<WeatherRepository>(context);

            return AppCubit(
              treeRepository: _treeRepository,
              authRepository: _authRepository,
              gardenRepository: _gardenRepository,
              taskRepository: _taskRepository,
              processRepository: _processRepository,
              userRepository: _userRepository,
              farmerRepository: _farmerRepository,
              weatherRepository: _weatherRepository,
            );
          }),
          BlocProvider<NavigationCubit>(create: (context) => _navigationCubit!),
          BlocProvider(create: (context) {
            final _notifyRepo =
                RepositoryProvider.of<NotificationRepository>(context);
            return NotificationManagementCubit(repository: _notifyRepo);
          }),

          // BlocProvider<DynamicConfigCubit>(
          //     create: (context) => _dynamicConfigCubit),
        ],
        child: BlocListener<AppCubit, AppState>(
          listener: (context, state) {},
          child: OverlaySupport(child: materialApp()),
        ),
        // child: materialApp(),
      ),
    );
  }

  GetMaterialApp materialApp() {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
    return GetMaterialApp(
      navigatorKey: appNavigatorKey,
      title: AppConfig.appName,
      //đã sửa hardcode
      theme: AppThemes.theme,
      onGenerateRoute: Application.router!.generator,
      initialRoute: Routes.root,
      navigatorObservers: <NavigatorObserver>[
        NavigationObserver(navigationCubit: _navigationCubit),
      ],
      localizationsDelegates: [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        S.delegate,
      ],
      supportedLocales: S.delegate.supportedLocales,
      builder: (context, child) {
        return GestureDetector(
          onTap: () {
            // When running in iOS, dismiss the keyboard when any Tap happens outside a TextField
            /*if (Platform.isIOS) */ hideKeyboard(context);
          },
          child: MediaQuery(
            child: child!,
            data: MediaQuery.of(context).copyWith(textScaleFactor: 1.0),
          ),
        );
      },
    );
  }

  void hideKeyboard(BuildContext context) {
    FocusScopeNode currentFocus = FocusScope.of(context);
    if (!currentFocus.hasPrimaryFocus && currentFocus.focusedChild != null) {
      FocusManager.instance.primaryFocus!.unfocus();
    }
  }
}
