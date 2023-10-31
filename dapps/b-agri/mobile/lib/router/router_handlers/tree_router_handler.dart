import 'package:fluro/fluro.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_base/repositories/tree_repository.dart';
import 'package:flutter_base/ui/pages/tree_management/create_tree/create_tree_cubit.dart';
import 'package:flutter_base/ui/pages/tree_management/create_tree/create_tree_page.dart';
import 'package:flutter_base/ui/pages/tree_management/tree_detail/tree_detail_cubit.dart';
import 'package:flutter_base/ui/pages/tree_management/tree_detail/tree_detail_page.dart';
import 'package:flutter_base/ui/pages/tree_management/update_tree/update_tree_cubit.dart';
import 'package:flutter_base/ui/pages/tree_management/update_tree/update_tree_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

Handler treeCreateHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      final treeRepository = RepositoryProvider.of<TreeRepository>(context);
      return CreateTreeCubit(treeRepository: treeRepository);
    },
    child: CreateTreePage(),
  );
});

Handler treeUpdateHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  TreeUpdateArgument args = context!.settings!.arguments as TreeUpdateArgument;
  return BlocProvider(
    create: (context) {
      final treeRepository = RepositoryProvider.of<TreeRepository>(context);
      return UpdateTreeCubit(treeRepository: treeRepository);
    },
    child: UpdateTreePage(
      tree_id: args.tree_id,
      name: args.name,
      description: args.description,
    ),
  );
});

Handler treeDetailHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  TreeDetailArgument args = context!.settings!.arguments as TreeDetailArgument;
  return BlocProvider(
    create: (context) {
      final treeRepository = RepositoryProvider.of<TreeRepository>(context);
      return TreeDetailCubit(treeRepository: treeRepository);
    },
    child: TreeDetailPage(
      tree_id: args.tree_id,
      name: args.name,
      description: args.description,
    ),
  );
});
