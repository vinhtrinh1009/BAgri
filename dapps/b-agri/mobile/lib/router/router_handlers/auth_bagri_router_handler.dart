import 'package:fluro/fluro.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_base/repositories/auth_repository.dart';
import 'package:flutter_base/repositories/user_repository.dart';
import 'package:flutter_base/ui/pages/auth/change_password/change_password_cubit.dart';
import 'package:flutter_base/ui/pages/auth/change_password/change_password_page.dart';
import 'package:flutter_base/ui/pages/auth/forgot_password/forgot_password_cubit.dart';
import 'package:flutter_base/ui/pages/auth/forgot_password/forgot_password_page.dart';
import 'package:flutter_base/ui/pages/auth/login/login_cubit.dart';
import 'package:flutter_base/ui/pages/auth/login/login_page.dart';
import 'package:flutter_base/ui/pages/auth/register/register_page.dart';
import 'package:flutter_base/ui/pages/auth/register/registry_cubit.dart';
import 'package:flutter_base/ui/pages/splash/bagri_splash_page.dart';

import 'package:flutter_bloc/flutter_bloc.dart';

Handler bagriSplashHandler = new Handler(
  handlerFunc: (BuildContext? context, Map<String, List<String>> params) =>
      SplashPage(),
);

Handler loginHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      final repository = RepositoryProvider.of<AuthRepository>(context);
      final userRepo = RepositoryProvider.of<UserRepository>(context);
      return LoginCubit(repository: repository, userRepository: userRepo);
    },
    child: LoginPage(),
  );
});

Handler changePasswordHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      final repository = RepositoryProvider.of<AuthRepository>(context);
      return ChangePasswordCubit(repository: repository);
    },
    child: ChangePasswordPage(),
  );
});

Handler forgotPasswordHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      final repository = RepositoryProvider.of<AuthRepository>(context);
      return ForgotPasswordCubit(repository: repository);
    },
    child: ForgotPasswordPage(),
  );
});

Handler registryHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      final repository = RepositoryProvider.of<AuthRepository>(context);
      return RegistryCubit(repository: repository);
    },
    child: RegistryPage(),
  );
});
