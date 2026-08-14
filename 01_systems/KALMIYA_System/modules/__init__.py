try:
    from .todo_manager import TODOManager
except Exception:  # pragma: no cover - optional feature dependency
    TODOManager = None

try:
    from .emotion_voice import EmotionVoice
except Exception:
    EmotionVoice = None

try:
    from .notas_rapidas import NotasRapidas
except Exception:
    NotasRapidas = None

try:
    from .habitos import Habitos
except Exception:
    Habitos = None

try:
    from .pomodoro_timer import PomodoroTimer
except Exception:
    PomodoroTimer = None

try:
    from .calendar_sync import CalendarSync
except Exception:
    CalendarSync = None

try:
    from .email_integration import EmailIntegration
except Exception:
    EmailIntegration = None

try:
    from .reminder_system import ReminderSystem
except Exception:
    ReminderSystem = None

try:
    from .health_tracker import HealthTracker
except Exception:
    HealthTracker = None

try:
    from .sleep_monitor import SleepMonitor
except Exception:
    SleepMonitor = None

try:
    from .expense_tracker import ExpenseTracker
except Exception:
    ExpenseTracker = None

try:
    from .budget_analyzer import BudgetAnalyzer
except Exception:
    BudgetAnalyzer = None

try:
    from .weather_integration import WeatherIntegration
except Exception:
    WeatherIntegration = None

try:
    from .language_learning import LanguageLearning
except Exception:
    LanguageLearning = None

try:
    from .course_recommender import CourseRecommender
except Exception:
    CourseRecommender = None

try:
    from .reading_list import ReadingListManager
except Exception:
    ReadingListManager = None

try:
    from .music_playlist import MusicPlaylistGenerator
except Exception:
    MusicPlaylistGenerator = None

try:
    from .movie_recommender import MovieRecommender
except Exception:
    MovieRecommender = None

try:
    from .gaming_mode import GamingMode
except Exception:
    GamingMode = None

try:
    from .podcast_manager import PodcastManager
except Exception:
    PodcastManager = None

try:
    from .book_recommender import BookRecommender
except Exception:
    BookRecommender = None

try:
    from .smart_home_control import SmartHomeControl
except Exception:
    SmartHomeControl = None

try:
    from .light_management import LightManagement
except Exception:
    LightManagement = None

try:
    from .temperature_control import TemperatureControl
except Exception:
    TemperatureControl = None

try:
    from .device_automation import DeviceAutomation
except Exception:
    DeviceAutomation = None

try:
    from .energy_monitor import EnergyMonitor
except Exception:
    EnergyMonitor = None

try:
    from .trip_planner import TripPlanner
except Exception:
    TripPlanner = None

try:
    from .navigation_helper import NavigationHelper
except Exception:
    NavigationHelper = None

try:
    from .local_explorer import LocalExplorer
except Exception:
    LocalExplorer = None

try:
    from .travel_budget import TravelBudget
except Exception:
    TravelBudget = None

try:
    from .multi_language_support import MultiLanguageSupport
except Exception:
    MultiLanguageSupport = None

try:
    from .gesture_recognition import GestureRecognition
except Exception:
    GestureRecognition = None

try:
    from .emotion_detection import EmotionDetection
except Exception:
    EmotionDetection = None

try:
    from .translation_realtime import TranslationRealTime
except Exception:
    TranslationRealTime = None

try:
    from .conference_mode import ConferenceMode
except Exception:
    ConferenceMode = None

try:
    from .activity_reports import ActivityReports
except Exception:
    ActivityReports = None

try:
    from .performance_metrics import PerformanceMetrics
except Exception:
    PerformanceMetrics = None

try:
    from .productivity_stats import ProductivityStats
except Exception:
    ProductivityStats = None

try:
    from .weekly_summaries import WeeklySummaries
except Exception:
    WeeklySummaries = None

try:
    from .custom_dashboards import CustomDashboards
except Exception:
    CustomDashboards = None

try:
    from .social_media_sync import SocialMediaSync
except Exception:
    SocialMediaSync = None

try:
    from .cloud_storage_sync import CloudStorageSync
except Exception:
    CloudStorageSync = None

try:
    from .database_backup import DatabaseBackup
except Exception:
    DatabaseBackup = None

try:
    from .api_connectors import APIConnectors
except Exception:
    APIConnectors = None

try:
    from .webhook_support import WebhookSupport
except Exception:
    WebhookSupport = None

try:
    from .system_control import SystemControl
except Exception:
    SystemControl = None

try:
    from .daily_activities import DailyActivities
except Exception:
    DailyActivities = None

try:
    from .adso_study_mode import ADSOStudyMode
except Exception:
    ADSOStudyMode = None

__all__ = [
    'TODOManager',
    'EmotionVoice',
    'NotasRapidas',
    'Habitos',
    'PomodoroTimer',
    'CalendarSync',
    'EmailIntegration',
    'ReminderSystem',
    'HealthTracker',
    'SleepMonitor',
    'ExpenseTracker',
    'BudgetAnalyzer',
    'WeatherIntegration',
    'LanguageLearning',
    'CourseRecommender',
    'ReadingListManager',
    'MusicPlaylistGenerator',
    'MovieRecommender',
    'GamingMode',
    'PodcastManager',
    'BookRecommender',
    'SmartHomeControl',
    'LightManagement',
    'TemperatureControl',
    'DeviceAutomation',
    'EnergyMonitor',
    'TripPlanner',
    'NavigationHelper',
    'LocalExplorer',
    'TravelBudget',
    'MultiLanguageSupport',
    'GestureRecognition',
    'EmotionDetection',
    'TranslationRealTime',
    'ConferenceMode',
    'ActivityReports',
    'PerformanceMetrics',
    'ProductivityStats',
    'WeeklySummaries',
    'CustomDashboards',
    'SocialMediaSync',
    'CloudStorageSync',
    'DatabaseBackup',
    'APIConnectors',
    'WebhookSupport',
    'SystemControl',
    'DailyActivities',
    'ADSOStudyMode',
]
