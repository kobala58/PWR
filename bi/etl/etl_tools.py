import pandas as pd


def create_dim_company(df):
    dim_company = df[['company_name', 'company_url', 'company_size']].drop_duplicates().reset_index(drop=True)
    dim_company['company_id'] = dim_company.index + 1
    return dim_company


def create_dim_location(df):
    dim_location = df[['street', 'city', 'country_code', 'latitude', 'longitude']].drop_duplicates().reset_index(
        drop=True)
    dim_location['location_id'] = dim_location.index + 1
    return dim_location


def create_dim_skills(df):
    skills_expanded = df.explode('skills')[['id', 'skills']]
    skills_expanded = pd.concat([skills_expanded.drop(['skills'], axis=1), skills_expanded['skills'].apply(pd.Series)],
                                axis=1)
    skills_expanded = skills_expanded.rename(
        columns={'name': 'skill_name', 'level': 'skill_level'}).drop_duplicates().reset_index(drop=True)

    dim_skills = skills_expanded[['skill_name', 'skill_level']].drop_duplicates().reset_index(drop=True)
    dim_skills['skill_id'] = dim_skills.index + 1
    return dim_skills, skills_expanded


def create_employmet_dim(df):
    dim_emp = df[['employment_type']].drop_duplicates().reset_index(
        drop=True)
    dim_emp['employment_type_id'] = dim_emp.index + 1
    return dim_emp


def create_workplace_dim(df):
    dim_workplace = df[['workplace_type']].drop_duplicates().reset_index(
        drop=True)
    dim_workplace['workplace_type_id'] = dim_workplace.index + 1
    return dim_workplace


def create_fact_table(df, dim_company, dim_location, dim_workplace, dim_emp):
    df = df.merge(dim_company, on=['company_name', 'company_url', 'company_size'], how='left')
    df = df.merge(dim_location, on=['street', 'city', 'country_code', 'latitude', 'longitude'], how='left')
    df = df.merge(dim_workplace, on=['workplace_type'], how='inner')
    df = df.merge(dim_emp, on=['employment_type'], how='inner')

    print(df.head())

    fact_df = df
    return fact_df
