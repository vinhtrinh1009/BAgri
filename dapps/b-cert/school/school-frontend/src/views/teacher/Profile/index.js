import { Grid } from "@material-ui/core";
import Page from "src/shared/Page";
import AvatarBar from "./AvatarBar";
import ProfileForm from "./ProfileForm";

export default function TeacherProfile() {
    return (
        <Page title="Thông tin cá nhân">
            <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                    <ProfileForm></ProfileForm>
                </Grid>
                <Grid item xs={12} md={4}>
                    <AvatarBar></AvatarBar>
                </Grid>
            </Grid>
        </Page>
    );
}
