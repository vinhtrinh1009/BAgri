cp lib/configs/app_config.dart apk-build/app_config.dart

if [[ $# -eq 0 ]] ;
then
    echo 'Missed the app version';
    exit 1;
else 
    # clean and install dependencies;
    flutter clean
    
    flutter pub get

    flutter pub run intl_utils:generate

    flutter pub run build_runner build --delete-conflicting-outputs

    echo 'Start build with Staging';
    # build with staging config;
    cp apk-build/app_config_staging.dart lib/configs/app_config.dart

    flutter build apk --flavor bag

    cp build/app/outputs/flutter-apk/app-bag-release.apk ~/Desktop/app-staging-$1.apk

    # revert app config;
    cp apk-build/app_config.dart lib/configs/app_config.dart
    
    rm apk-build/app_config.dart
    
    echo '\nHave nice day :)';
fi