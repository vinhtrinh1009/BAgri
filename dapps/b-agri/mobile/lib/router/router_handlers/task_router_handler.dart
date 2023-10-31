import 'package:fluro/fluro.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/repositories/task_repository.dart';
import 'package:flutter_base/repositories/upload_repository.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/add_garden_task/add_garden_task_cubit.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/add_garden_task/add_garden_task_page.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/garden_task_cubit.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/garden_task_page.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/update_garden_task/update_garden_task_cubit.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/update_garden_task/update_garden_task_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

Handler taskCreateHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  GardenTaskCreateArgument args =
      context!.settings!.arguments as GardenTaskCreateArgument;

  return BlocProvider(
    create: (context) {
      final taskRepository = RepositoryProvider.of<TaskRepository>(context);
      final uploadRepo = RepositoryProvider.of<UploadRepository>(context);

      return AddGardenTaskCubit(
          taskRepository: taskRepository, uploadRepo: uploadRepo);
    },
    child: AddGardenTaskPage(
      name: args.name,
      season_id: args.season_id,
    ),
  );
});

Handler gardenTaskHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  GardenTaskArgument args = context!.settings!.arguments as GardenTaskArgument;
  return BlocProvider(
    create: (context) {
      final taskRepository = RepositoryProvider.of<TaskRepository>(context);
      return GardenTaskCubit(taskRepository: taskRepository);
    },
    child: GardenTaskPage(
      garden_id: args.garden_id,
      name: args.name,
      process_id: args.process_id,
      season_id: args.season_id,
    ),
  );
});

Handler taskUpdateHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  GardenTaskUpdateArgument args =
      context!.settings!.arguments as GardenTaskUpdateArgument;

  return BlocProvider(
    create: (context) {
      final taskRepository = RepositoryProvider.of<TaskRepository>(context);
      final uploadRepo = RepositoryProvider.of<UploadRepository>(context);

      return UpdateGardenTaskCubit(
          taskRepository: taskRepository, uploadRepo: uploadRepo);
    },
    child: UpdateGardenTaskPage(
      name: args.name,
      task_id: args.task_id,
      season_id: args.season_id,
    ),
  );
});
