import 'package:fluro/fluro.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_base/repositories/farmer_repository.dart';
import 'package:flutter_base/ui/pages/farmers_management/add_employee/employee_adding_cubit.dart';
import 'package:flutter_base/ui/pages/farmers_management/add_employee/employee_adding_page.dart';
import 'package:flutter_base/ui/pages/farmers_management/employee_detail/employee_detail_cubit.dart';
import 'package:flutter_base/ui/pages/farmers_management/employee_detail/employee_detail_page.dart';
import 'package:flutter_base/ui/pages/farmers_management/employee_management_cubit.dart';
import 'package:flutter_base/ui/pages/farmers_management/employee_management_page.dart';
import 'package:flutter_base/ui/pages/farmers_management/update_employee/employee_updating_cubit.dart';
import 'package:flutter_base/ui/pages/farmers_management/update_employee/employee_updating_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

Handler employeeManagementHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      FarmerRepository farmerRepository =
          RepositoryProvider.of<FarmerRepository>(context);
      return EmployeeManagementCubit(farmerRepository: farmerRepository);
    },
    child: EmployeeManagementPage(),
  );
});

Handler employeeAddingHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      FarmerRepository farmerRepository =
          RepositoryProvider.of<FarmerRepository>(context);
      return EmployeeAddingCubit(farmerRepository: farmerRepository);
    },
    child: EmployeeAddingPage(),
  );
});

Handler employeeUpdatingHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  String farmerId = context!.settings!.arguments as String;
  return BlocProvider(
    create: (context) {
      FarmerRepository farmerRepository =
          RepositoryProvider.of<FarmerRepository>(context);
      return EmployeeUpdatingCubit(farmerRepository: farmerRepository);
    },
    child: EmployeeUpdatingPage(
      farmerId: farmerId,
    ),
  );
});

Handler employeeDetailHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  String farmerId = context!.settings!.arguments as String;
  return BlocProvider(
    create: (context) {
      FarmerRepository farmerRepository =
          RepositoryProvider.of<FarmerRepository>(context);
      return EmployeeDetailCubit(farmerRepository: farmerRepository);
    },
    child: EmployeeDetailPage(
      farmerId: farmerId,
    ),
  );
});
