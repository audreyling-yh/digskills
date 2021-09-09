import os
import config
from src.ConvertMCFJobsToBert import ConvertMCFJobsToBert
from src.ConvertSSGTscToBert import ConvertSSGTscToBert
from src.ExploreExtensiveMargin import ExploreExtensiveMargin
from src.ExploreSSOC1DRoles import ExploreSSOC1DRoles
from src.ExploreSSOC1DSkills import ExploreSSOC1DSkills
from src.ExploreSSOC4DSkills import ExploreSSOC4DSkills
from src.ExploreSubtrackTsc import ExploreSubtrackTsc
from src.ExploreRolesAndSkills import ExploreRolesAndSkills
from src.GetIctSkills import GetIctSkills
from src.MapIctJobsToSsoc import MapIctJobsToSsoc
from src.MapMCFJobsToSsoc import MapMCFJobsToSsoc
from src.MatchMCFJobsToIctSkills import MatchMCFJobsToIctSkills
from src.MatchMCFJobsToIctTracks import MatchMCFJobsToIctTracks
from src.SplitMCFJobs import SplitMCFJobs

# Create folders
filepaths = config.filepaths
folders = list(set([filepaths[k]['folder'] for k in filepaths.keys()]))
for i in folders:
    os.makedirs(i, exist_ok=True)

# Get filepaths
original_ssg = filepaths['ssg_skills_original']['folder'] + filepaths['ssg_skills_original']['filename']
original_role_to_tsc = filepaths['role_to_tsc']['folder'] + filepaths['role_to_tsc']['filename']
original_ssoc_index = filepaths['ssoc_index_original']['folder'] + filepaths['ssoc_index_original']['filename']
original_ssoc2015_to_2020 = filepaths['ssoc2015_to_2020_original']['folder'] + filepaths['ssoc2015_to_2020_original'][
    'filename']

dau_ssoc_index = filepaths['ssoc_index_dau']['folder'] + filepaths['ssoc_index_dau']['filename']

img = filepaths['img']['folder'] + filepaths['img']['filename']
img_data = filepaths['img_data']['folder'] + filepaths['img_data']['filename']

ssg_with_bert = filepaths['ssg_skills_bert']['folder'] + filepaths['ssg_skills_bert']['filename']

digital_skills = filepaths['digital_skills']['folder'] + filepaths['digital_skills']['filename']
digital_skills_filtered = filepaths['digital_skills_filtered']['folder'] + filepaths['digital_skills_filtered'][
    'filename']

ict_jobs_with_ssoc = filepaths['digital_jobs_ssoc']['folder'] + filepaths['digital_jobs_ssoc']['filename']
ict_jobs_with_dau_ssoc = filepaths['digital_jobs_dau_ssoc']['folder'] + filepaths['digital_jobs_dau_ssoc']['filename']

mcf_jobpostings_ssoc = filepaths['mcf_jobpostings_ssoc']['folder'] + filepaths['mcf_jobpostings_ssoc']['filename']
mcf_jobpostings_bert = filepaths['mcf_jobpostings_bert']['folder'] + filepaths['mcf_jobpostings_bert']['filename']
mcf_jobpostings_bert_split = filepaths['mcf_jobpostings_bert_split']['folder'] + \
                             filepaths['mcf_jobpostings_bert_split']['filename']
mcf_jobpostings_digskills = filepaths['mcf_jobpostings_digital_skills']['folder'] + \
                            filepaths['mcf_jobpostings_digital_skills']['filename']
mcf_jobpostings_digtracks = filepaths['mcf_jobpostings_digital_tracks']['folder'] + \
                            filepaths['mcf_jobpostings_digital_tracks']['filename']

cosine = filepaths['cosine_matrix']['folder'] + filepaths['cosine_matrix']['filename']

analysis=filepaths['analysis']['folder']+filepaths['analysis']['filename']

# Get folders
mcf_jobpostings_folder = filepaths['mcf_jobpostings_original']['folder']
mcf_jobpostings_ssoc_folder = filepaths['mcf_jobpostings_ssoc']['folder']
mcf_jobpostings_bert_folder = filepaths['mcf_jobpostings_bert']['folder']
mcf_jobpostings_bert_splitfolder = filepaths['mcf_jobpostings_bert_split']['folder']
mcf_jobpostings_digskills_folder = filepaths['mcf_jobpostings_digital_skills']['folder']
mcf_jobpostings_digtracks_folder = filepaths['mcf_jobpostings_digital_tracks']['folder']

if __name__ == '__main__':
    # # convert tsc-proficiency abilities list to Bert word embeddings
    # tsctobert = ConvertSSGTscToBert(original_ssg, ssg_with_bert)
    # tsctobert.run()

    # # tag each ICT skills framework job with an ssoc4d 2020 (dau mapping)
    # icttossoc = MapIctJobsToSsoc(original_role_to_tsc, original_ssoc_index, dau_ssoc_index, ict_jobs_with_dau_ssoc)
    # icttossoc.run()

    # # filter tsc-prof bert embeddings to include only ict/digital ones
    # tsctoict = GetIctSkills(ssg_with_bert, ict_jobs_with_dau_ssoc, digital_skills)
    # tsctoict.run()

    # # tag each job posting with ssoc4d/1d 2020 and AES sector of the hiring org, and remove non-PMET jobs
    # jobtossoc = MapMCFJobsToSsoc(mcf_jobpostings_folder, mcf_jobpostings_ssoc, original_ssoc2015_to_2020)
    # jobtossoc.run()

    # # get plots of tsc-proficiency and subtracks distribution, drops skills that are in too many tracks
    # exploresubtracktsc = ExploreSubtrackTsc(digital_skills, digital_skills_filtered, img)
    # exploresubtracktsc.run()

    # # combine all job description text files into a dataframe and obtain Bert embeddings for each job
    # # CAUTION: Will take about 1 day to run
    # jobtobert = ConvertMCFJobsToBert(mcf_jobpostings_ssoc_folder, mcf_jobpostings_bert)
    # jobtobert.run()

    # # Split large mcf job postings files into smaller files
    # splitjobs=SplitMCFJobs(mcf_jobpostings_bert_folder,mcf_jobpostings_bert_split)
    # splitjobs.run()

    # # get a list of ict skills matched to each job using cosine similarity of bert embeddings
    # # CAUTION: Will take about 3 hours
    # jobtoskills=MatchMCFJobsToIctSkills(digital_skills_filtered,mcf_jobpostings_bert_splitfolder,cosine,mcf_jobpostings_digskills)
    # jobtoskills.run()

    # # get main and subtracks of each job
    # jobtotracks=MatchMCFJobsToIctTracks(digital_skills_filtered,mcf_jobpostings_digskills_folder,mcf_jobpostings_digtracks)
    # jobtotracks.run()

    # # TODO: Redo analysis
    # # Extensive margin
    # exploreextensive = ExploreExtensiveMargin(img,analysis)
    # exploreextensive.run()

    # # analyse ict roles by SSOC1D
    # explore1droles = ExploreSSOC1DRoles(ict_jobs_with_ssoc, img_data)
    # explore1droles.run()

    # # analyse ict skills by SSOC1D
    # explore1dskills = ExploreSSOC1DSkills(img_data)
    # explore1dskills.run()

    # # analyse ict skills by SSOC4D
    # explore4dskills = ExploreSSOC4DSkills(analysis_largest_ssoc,
    #                                       analysis_postings_per_track,
    #                                       analysis_postings_per_subtrack,
    #                                       analysis_tracks_rankdelta,
    #                                       analysis_subtracks_rankdelta,
    #                                       analysis_tracks_per_posting,
    #                                       analysis_subtracks_per_posting,
    #                                       analysis_tracks_per_posting_delta,
    #                                       analysis_subtracks_per_posting_delta,
    #                                       analysis_skills_per_track,
    #                                       analysis_skills_per_subtrack,
    #                                       analysis_skills_per_track_delta,
    #                                       analysis_skills_per_subtrack_delta)
    # explore4dskills.run()

    # ## analyse ict jobs X skills
    # explorerolesskills = ExploreRolesAndSkills(ict_jobs_with_ssoc,
    #                                            analysis_largest_ssoc_ict,
    #                                            analysis_largest_ssoc_nonict,
    #                                            analysis_tracks_ict_rankdelta,
    #                                            analysis_subtracks_ict_rankdelta,
    #                                            analysis_tracks_nonict_rankdelta,
    #                                            analysis_subtracks_nonict_rankdelta,
    #                                            analysis_tracks_ict_per_posting_delta,
    #                                            analysis_subtracks_ict_per_posting_delta,
    #                                            analysis_tracks_nonict_per_posting_delta,
    #                                            analysis_subtracks_nonict_per_posting_delta,
    #                                            analysis_skills_per_track_ict_delta,
    #                                            analysis_skills_per_subtrack_ict_delta,
    #                                            analysis_skills_per_track_nonict_delta,
    #                                            analysis_skills_per_subtrack_nonict_delta)
    # explorerolesskills.run()
